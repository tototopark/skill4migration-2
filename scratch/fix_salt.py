import bcrypt

# List of hashes from db query
users = {
    "Alison": "$2y$10$ht9daTg8InrdheqcDncYGu2X3.Gcb4YBrGY7B0jvRRayKthIZ4x2G",
    "test": "$2y$10$i.FpxcqTVQyD8WK0QywTc.L1frPsVchbtdYkKt1y2zbgZ.Uxfh/bq"
}

passwords = ["password", "testpassword", "test", "1234", "123456", "admin", "pengelly", "alison", "Alison", "jumbo", "jumbodragonfly"]

def test_passwords():
    for name, hashed in users.items():
        # Replace $2y$ with $2b$
        fixed_hash = "$2b$" + hashed[4:]
        for pw in passwords:
            try:
                if bcrypt.checkpw(pw.encode('utf-8'), fixed_hash.encode('utf-8')):
                    print(f"MATCH: User '{name}' password is '{pw}'")
                    return
            except Exception as e:
                print(f"Error checking {pw}: {e}")

test_passwords()
