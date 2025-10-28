
from create_table.base_information import Users


def give_status (id_user:int , session):
    user = session.query(Users).filter(Users.id == id_user).first()
    if user:
        status = user.status
        return status
    else:
        raise ValueError(f"User with id {id_user} not found STATUS")



def give_age (id_user:int , session):
    user = session.query(Users).filter(Users.id == id_user).first()
    if user:
        our_age =user.age
        return our_age
    else:
        raise ValueError(f"User with id {id_user} not found ages")



def give_gender (id_user:int , session):
    user = session.query(Users).filter(Users.id == id_user).first()
    if not user:
        raise ValueError(f"User with id {id_user} not found")
    else:
        gender =user.gender
    return gender




def give_city_id_name (id_user: int, session):
    user = session.query(Users).filter(Users.id == id_user).first()
    if user:
        city_id = user.city_id
        city_name = user.city
        return city_id, city_name
    else:
        raise ValueError(f"User with id {id_user} not found")

