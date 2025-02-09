# TODO Choose and document the representation for tiles and grids
import numpy as np 
import random as rd

def print_tile():
    # TODO
    pass


def print_grid():
    # TODO
    pass


def generate_grid():
    # TODO
    pass


if __name__ == "__main__":
    # TODO
    # grid = generate_grid(...)
    # print_grid(...)
    pass


def is_grid_consistent():
    # TODO
    pass

def generate_case():
    
    A = np.zeros((3, 3))  
    A[1, 1] = 1
    n = rd.randint(2, 4)
    
    # Générer n valeurs distinctes entre 1 et 4 (les directions)
    L = rd.sample(range(1, 5), n)
    
    for direction in L:
        if direction == 1:  
            A[0][1] = 1
        elif direction == 2:  
            A[1][2] = 1
        elif direction == 3:  
            A[2][1] = 1
        elif direction == 4:  
            A[1][0] = 1
    
    return A

print(generate_case())

def generecolonne(C):
 
    B = np.zeros((3, 3))  
    B[1, 1] = 1  
    
    # Assurer la connexion avec la matrice précédente
    if C[2][1] == 1:  # Si la case du bas de C est 1, alors la case du haut de B doit être 1
        B[0][1] = 1
    else:
        B[0][1] = 0
    

    n = rd.randint(1, 3)
    L = rd.sample(range(1, 4), n)  

    for direction in L:
        if direction == 1:    
            B[1][2] = 1
        elif direction == 2:  
            B[2][1] = 1
        elif direction == 3:  
            B[1][0] = 1
    
    # Assurer qu'il y a au moins un chemin dans la tuile
    if np.sum(B) == 0:
        B[1, 1] = 1  # Assurer au moins un chemin central
    
    return B

def concatenate_multiple_tuiles(num_tuiles):
    # Générer la première tuile
    A = generate_case()
    
    # Stocker la matrice concaténée initialement avec A
    result = A
    
    # Générer et concaténer les matrices suivantes
    for _ in range(1, num_tuiles):
        B = generecolonne(A)  # Générer la tuile B connectée à la précédente A
        result = np.vstack((result, B))  # Concaténer A et B
        A = B  # B devient la nouvelle A pour la prochaine itération
    
    return result

# Exemple 
num_tuiles = 10  
grid = concatenate_multiple_tuiles(num_tuiles)
print("Grille concaténée de 10 tuiles :")
print(grid)
 

def generate_consistent_grid():
    # TODO
    pass


if __name__ == "__main__":
    # TODO
    # grid = generate_consistent_grid(...)
    # print_grid(...)
    # print(is_grid_consistent(...))
    pass

