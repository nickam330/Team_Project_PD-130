from create_table.create_session import*

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = sq.Column(sq.BIGINT, primary_key=True)
    age = sq.Column(sq.Integer, nullable=True)
    gender = sq.Column(sq.String, nullable=True)
    city = sq.Column(sq.VARCHAR(60), nullable=True)

    selected = relationship("Selected", secondary = 'users_selected', back_populates="users")


class Selected(Base):
    __tablename__ = 'selected'
    select_user_id = sq.Column(sq.BIGINT,primary_key=True ,nullable=False)
    link = sq.Column(sq.Text, nullable=False)

    users = relationship("Users", secondary = 'users_selected', back_populates = 'selected' )


class UsersSelected(Base):
    __tablename__ = 'users_selected'
    users_id = sq.Column(sq.BIGINT, sq.ForeignKey('users.id'),primary_key=True , nullable=False)
    selected_id = sq.Column(sq.BIGINT, sq.ForeignKey('selected.select_user_id'),primary_key=True , nullable=False)
    is_favourite = sq.Column(sq.Boolean, nullable=True)

