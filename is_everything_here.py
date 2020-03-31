import os, glob

required = [
    "non_target_dev",
    "non_target_train",
    "target_dev",
    "target_train",
    "ikrlib.py",
]

ok = True
for f in required:
    if(not glob.glob(f)):
        print(f"Missing: {f}")
        ok = False

if(ok):
    print("All required files/directories found")
    exit(0)
else:
    print("Not all required files found")
    exit(1)