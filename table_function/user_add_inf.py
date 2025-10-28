from create_table.base_information import Users




def add_user_id (id_user, session):
    user_our = Users(id = id_user)
    session.add(user_our)
    session.commit()



def add_age (id_user:int ,our_age:int, session):
    user = session.query(Users).filter(Users.id == id_user).first()
    if user:
        user.age = our_age
        session.commit()



def add_gender (id_user:int ,user_gender:str, session):
    user_gender_stand = user_gender.lower()
    user = session.query(Users).filter(Users.id == id_user).first()
    if not user:
        raise ValueError(f"User with id {id_user} not found")
    if user_gender_stand in ('male', 'female'):
        user.gender = user_gender_stand
        session.commit()
    else:
        raise ValueError(f"gender {user_gender_stand} not found")



def add_city_name_int (id_user: int, our_city:str,city_id:int, session):
    our_city_stand = our_city.lower()
    user = session.query(Users).filter(Users.id == id_user).first()
    if user:
        user.city_id = city_id
        user.city = our_city_stand
        session.commit()
    else:
        raise ValueError(f"User with id {id_user} not found")

def add_status (id_user:int ,user_status:int,session):
    user = session.query(Users).filter(Users.id == id_user).first()
    if user:
        user.status = user_status
        session.commit()
    else:
        raise ValueError(f"User with id {id_user} not found")
