import psycopg2
from information import *
from create_table.create_session import*

def show_favourite(user_id):
    conn = psycopg2.connect( dbname= basadate_name, user=login_postgres, password=password_postgres)
    with conn.cursor() as cursor:
        cursor.execute(
                        """SELECT s.link
                                FROM users u
                                LEFT JOIN users_selected us ON us.users_id = u.id
                                LEFT JOIN selected s ON s.select_user_id = us.selected_id
                                where us.is_favourite = TRUE
                                    AND u.id = %s      
                                GROUP BY s.link;""",(user_id,))
        info = cursor.fetchall()
    conn.close()
    return info


def add_favourite(user_id, select_id):
    error = None
    conn = psycopg2.connect( dbname= basadate_name, user=login_postgres, password=password_postgres)
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                            """UPDATE public.users_selected us
                                    SET is_favourite = TRUE
                                    FROM public.users u
                                    WHERE us.users_id = u.id
                                      AND u.id = %s     
                                      AND us.selected_id = %s;""",(user_id, select_id))
            conn.commit()
    except Exception as ex:
        error = ex
    finally:
        if conn:
            conn.close()
    return error
