import sys
import base64
from pathlib import Path
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

if len(sys.argv) != 2:
    print("Usage: python scripts/generate_proof.py <COMMIT_HASH>")
    sys.exit(1)

root = Path(__file__).resolve().parent.parent

# Load keys
with open(root / "student_private.pem", "rb") as f:
    priv = serialization.load_pem_private_key(f.read(), password=None)
with open(root / "instructor_public.pem", "rb") as f:
    pub = serialization.load_pem_public_key(f.read())

# Sign the Commit Hash (RSA-PSS)
sig = priv.sign(
    sys.argv[1].encode('utf-8'),
    padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
    hashes.SHA256()
)

# Encrypt the Signature (RSA-OAEP)
enc = pub.encrypt(
    sig,
    padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)

print(base64.b64encode(enc).decode('ascii'))