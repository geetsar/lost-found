from pywebpush import generate_vapid_private_key, generate_vapid_public_key

private_key = generate_vapid_private_key()
public_key = generate_vapid_public_key(private_key)

print("PUBLIC KEY:", public_key)
print("PRIVATE KEY:", private_key)
     