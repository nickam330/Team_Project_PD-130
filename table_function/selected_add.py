from create_table.base_information import Users, Selected



def add_selected (user_id:int, selected_id:int, link:str, session):
    user = session.query(Users).filter(Users.id==user_id).first()
    selected = session.query(Selected).filter(Selected.select_user_id == selected_id).first()
    if not user:
        raise ValueError(f"User with id {user_id} not found")
    if selected:
        selected.link = link
        if selected not in user.selected:
            user.selected.append(selected)

    else:
        selected = Selected(select_user_id = selected_id, link = link)
        session.add(selected)
        user.selected.append(selected)
    session.commit()


def link_list(user_id: int, session):
    user = session.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise ValueError(f"User with id {user_id} not found")
    return [sel.select_user_id for sel in user.selected]





