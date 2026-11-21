notas = [7.5, 8.0, 6.5, 9.0]

# soma tudo e divide pela quantidade
media = sum(notas) / len(notas)

print(f"Notas: {notas}")
print(f"Média: {media:.2f}")
if media >= 7:
    print("Aprovado!")
