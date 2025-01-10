from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Utility function to load and save data
FILE_PATH = "data.json"

def load_data():
    try:
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)

# CRUD Operations

# 1. Create a new user
@csrf_exempt
def create_user(request):
    if request.method == "POST":
        new_user = json.loads(request.body)  # Parse JSON payload
        data = load_data()
        
        # Check if email already exists
        if any(user["email"] == new_user["email"] for user in data):
            return JsonResponse({"message": "Email already exists!"}, status=400)
        
        # Generate new user ID
        new_user["id"] = len(data) + 1
        data.append(new_user)
        save_data(data)
        return JsonResponse(new_user, status=201)

# 2. Read all users
def read_users(request):
    if request.method == "GET":
        data = load_data()
        return JsonResponse(data, safe=False)

# 3. Read a single user by ID
def read_user_by_id(request, user_id):
    if request.method == "GET":
        data = load_data()
        user = next((user for user in data if user["id"] == user_id), None)
        if user:
            return JsonResponse(user, safe=False)
        return JsonResponse({"message": "User not found!"}, status=404)

# 4. Update a user by ID
def update_user(request, user_id):
    if request.method == "PUT":
        updated_user = json.loads(request.body)
        data = load_data()
        
        for user in data:
            if user["id"] == user_id:
                user.update(updated_user)  # Update user fields
                save_data(data)
                return JsonResponse(user)
        
        return JsonResponse({"message": "User not found!"}, status=404)

# 5. Delete a user by ID
def delete_user(request, user_id):
    if request.method == "DELETE":
        data = load_data()
        new_data = [user for user in data if user["id"] != user_id]
        
        if len(data) == len(new_data):
            return JsonResponse({"message": "User not found!"}, status=404)
        
        save_data(new_data)
        return JsonResponse({"message": "User deleted successfully!"}, status=200)
