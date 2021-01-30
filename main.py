from expression import Expression

if __name__ == "__main__":
    e = Expression("m*t'+t*m'+t*m")
    e.display()
    
    e.add_term("m+t")
    e.display()