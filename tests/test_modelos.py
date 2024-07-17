from app.modelos import Director,DAO_CSV_Director

def test_create_director():
    director = Director("Kevin Heredia") 
    assert director.nombre == "Kevin Heredia"
    assert director.id == -1

def test_dao_directores_traer_todos():
    dao = DAO_CSV_Director("tests/data/directores.csv")
    directores = dao.todos()

    assert len(directores) == 8
    assert directores[7] == Director("Charlie Chaplin", 8)