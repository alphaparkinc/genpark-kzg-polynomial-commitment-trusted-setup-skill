from client import KZGCommitment

kzg = KZGCommitment(s=4, degree=3)
poly = [2, 3, 5]  # 2 + 3x + 5x^2

commit = kzg.commit(poly)
eval_at_3 = kzg.evaluate(poly, z=3)
print(f"Commitment: {commit}, f(3) = {eval_at_3}")
