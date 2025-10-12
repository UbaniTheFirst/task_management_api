from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import UserSerializer, TaskSerializer, TaskCreateUpdateSerializer


# ==================== Authentication Views ====================

class RegisterView(generics.CreateAPIView):
    """Register a new user."""
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create token for the new user
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'token': token.key,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Login user and return token."""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Please provide both username and password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        }, status=status.HTTP_200_OK)
    
    return Response(
        {'error': 'Invalid credentials'},
        status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Logout user by deleting their token."""
    try:
        request.user.auth_token.delete()
        return Response(
            {'message': 'Successfully logged out'},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


# ==================== Task Views ====================

class TaskListCreateView(generics.ListCreateAPIView):
    """
    List all tasks for the authenticated user or create a new task.
    Supports filtering by status, priority, and due_date.
    Supports sorting by due_date and priority.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'due_date']
    ordering_fields = ['due_date', 'priority', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Return only tasks belonging to the current user."""
        return Task.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Use different serializer for POST requests."""
        if self.request.method == 'POST':
            return TaskCreateUpdateSerializer
        return TaskSerializer
    
    def perform_create(self, serializer):
        """Save the task with the current user."""
        serializer.save(user=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific task.
    Users can only access their own tasks.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return only tasks belonging to the current user."""
        return Task.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Use different serializer for PUT/PATCH requests."""
        if self.request.method in ['PUT', 'PATCH']:
            return TaskCreateUpdateSerializer
        return TaskSerializer
    
    def perform_update(self, serializer):
        """Prevent updating completed tasks."""
        if self.get_object().status == 'Completed':
            return Response(
                {'error': 'Cannot edit a completed task. Mark it as incomplete first.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_complete(request, pk):
    """Mark a task as complete."""
    try:
        task = Task.objects.get(pk=pk, user=request.user)
    except Task.DoesNotExist:
        return Response(
            {'error': 'Task not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    task.mark_complete()
    serializer = TaskSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_incomplete(request, pk):
    """Mark a task as incomplete."""
    try:
        task = Task.objects.get(pk=pk, user=request.user)
    except Task.DoesNotExist:
        return Response(
            {'error': 'Task not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    task.mark_incomplete()
    serializer = TaskSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)