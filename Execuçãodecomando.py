#tratamento de notas 
#Condicional composta, entrada pelo usuario


nota = float(input("Qual a sua nota?"))
if nota <= 0 or nota >=10:
    print ("Erro: Nota invalid. Digite um valor entre 0 e 10")
elif nota >= 7:
    print("aprovado")
elif nota <= 6.9:
    print("Recuperação")
else:
    print("Reprovado")
