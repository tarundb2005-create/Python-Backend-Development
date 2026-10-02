from app.security import hash_password, verify_password

hashed = hash_password("mypassword123")

print(hashed)
print(verify_password("mypassword123", hashed))
print(verify_password("wrongpassword", hashed))