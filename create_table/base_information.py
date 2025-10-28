from create_table.create_session import *

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = sq.Column(sq.BIGINT, primary_key=True, autoincrement=False)
    age = sq.Column(sq.Integer, nullable=True)
    gender = sq.Column(sq.String, nullable=True)
    city = sq.Column(sq.VARCHAR(60), nullable=True)
    city_id = sq.Column(sq.Integer, nullable=True)
    status = sq.Column(sq.Integer, default=0)
    date_of_key = sq.Column(sq.DateTime, nullable=True)
    expires_in = sq.Column(sq.Integer, nullable=True)
    _device_id = sq.Column(sq.Text(), nullable=True)
    _access_token_encrypted = sq.Column(
        "access_token", sq.Text(), nullable=True)
    _refresh_token_encrypted = sq.Column(
        "refresh_token", sq.Text(), nullable=True)

    selected = relationship(
        "Selected",
        secondary='users_selected',
        back_populates="users")

    @property
    def device_id(self):
        if self._device_id:
            return fernet.decrypt(self._device_id.encode()).decode()
        return None

    @device_id.setter
    def device_id(self, value):
        if value:
            self._device_id = fernet.encrypt(value.encode()).decode()
        else:
            self._device_id = None

    @property
    def access_token(self):
        if self._access_token_encrypted:
            return fernet.decrypt(
                self._access_token_encrypted.encode()).decode()
        return None

    @access_token.setter
    def access_token(self, value):
        if value:
            self._access_token_encrypted = fernet.encrypt(
                value.encode()).decode()
        else:
            self._access_token_encrypted = None

    @property
    def refresh_token(self):
        if self._refresh_token_encrypted:
            return fernet.decrypt(
                self._refresh_token_encrypted.encode()).decode()
        return None

    @refresh_token.setter
    def refresh_token(self, value):
        if value:
            self._refresh_token_encrypted = fernet.encrypt(
                value.encode()).decode()
        else:
            self._refresh_token_encrypted = None


class Selected(Base):
    __tablename__ = 'selected'
    select_user_id = sq.Column(sq.BIGINT, primary_key=True, nullable=False)
    link = sq.Column(sq.Text, nullable=False)

    users = relationship(
        "Users",
        secondary='users_selected',
        back_populates='selected')


class UsersSelected(Base):
    __tablename__ = 'users_selected'
    users_id = sq.Column(
        sq.BIGINT,
        sq.ForeignKey('users.id'),
        primary_key=True,
        nullable=False)
    selected_id = sq.Column(
        sq.BIGINT,
        sq.ForeignKey('selected.select_user_id'),
        primary_key=True,
        nullable=False)
    is_favourite = sq.Column(sq.Boolean, nullable=True)
