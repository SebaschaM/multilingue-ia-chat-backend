from src.database.db_pg import db
from src.models.conversations import Conversations
from src.models.users import Users
from src.models.clients import Clients
from src.models.requests import Requests
#from sqlalchemy import or_, and_
import json

from sqlalchemy import tablesample, func, extract, Column, Integer, DateTime, case


class DashBoardService:
    @classmethod
    def count_requests_by_month(cls):  # numero de solicitudes por mes
        try:
            condicion = True
            result = (
                db.session.query(
                    func.extract('month', Requests.created_at).label('mes'),
                    func.count().label('num_solicitudes')
                )
                .filter(condicion)
                .group_by(func.extract('month', Requests.created_at))
                .order_by('mes')
                .all()
            )
            result_dict = [
                    {'mes': int(row[0]), 'num_solicitudes': int(row[1])}
                    for row in result
                ]
            
            print(result_dict)
            return {
                "message": "Número de solicitudes por mes obtenidos exitosamente.",
                "success": True,
                "data": result_dict,
            }, 200

        
        except Exception as e:
            error_dict = {'error': f"Error en la consulta: {str(e)}"}
            return json.dumps(error_dict, indent=2)


    def count_clients_by_month(): #clientes registrados por mes
        try:
            condicion = True
            result = (
                db.session.query(
                    func.extract('month', Clients.created_at).label('mes'),
                    func.count().label('clients_registrados')
                )
                .filter(condicion)
                .group_by(func.extract('month', Clients.created_at))
                .order_by('mes')
                .all()
            )
            result_dict = [
                    {'mes': int(row[0]), 'clients_registrados': int(row[1])}
                    for row in result
                ]
            print(result_dict)
            return {
                "message": "Clientes registrados por mes obtenidos exitosamente.",
                "success": True,
                "data": result_dict,
            }, 200    
        except Exception as e:
            error_dict = {'error': f"Error en la consulta: {str(e)}"}
            return json.dumps(error_dict, indent=2)

    def total_attended_chats(): #total de chats atendidos
        try:
            result = (
                db.session.query(
                    func.count().label('total_chats_atendidos')
                )
                .filter(Conversations.state == 0)
                .all()
            )

            total_chats_atendidos = result[0][0] if result and result[0] else 0

            result_dict = [
                {'total_chats_atendidos': total_chats_atendidos}
            ]

            print(result_dict)

            return {
                "message": "Total de chats atendidos obtenido exitosamente.",
                "success": True,
                "data": result_dict,
            }, 200

        except Exception as e:
            error_dict = {'error': f"Error en la consulta: {str(e)}"}
            return json.dumps({
                "message": "Error al obtener el total de chats atendidos.",
                "success": False,
                "error": error_dict
            }, indent=2), 500

    def percentage_of_users_by_role(): # porcentaje de usuarios(agente y gerente)
        try:
            total_users = db.session.query(func.count()).select_from(Users).scalar()
            result = (
                db.session.query(
                    (func.count().filter(Users.role_id == 1) / total_users * 100).label('percentage_gerentes'),
                    (func.count().filter(Users.role_id == 2) / total_users * 100).label('percentage_agentes')
                )
                .first()
            )

            percentage_gerentes = float(result.percentage_gerentes) if result.percentage_gerentes else 0
            percentage_agentes = float(result.percentage_agentes) if result.percentage_agentes else 0

            result_dict = [
                {'percentage_gerentes': percentage_gerentes, 'percentage_agentes': percentage_agentes}
            ]
            print(result_dict)
            return {
                "message": "Porcentaje de usuarios obtenido exitosamente.",
                "success": True,
                "data": result_dict
            }, 200

        except Exception as e:
            error_dict = {'error': f"Error en la consulta: {str(e)}"}
            return json.dumps({
                "message": "Error al obtener el porcentaje de usuarios.",
                "success": False,
                "error": error_dict
            }, indent=2), 500
        

    def count_chats_by_hour(): #chat de la ultima hora
        try:
            result = (
                db.session.query(
                    func.date_trunc('hour', Conversations.created_at).label('hour'),
                    func.count().label('num_chats')
                )
                .group_by(func.date_trunc('hour', Conversations.created_at))
                .order_by('hour')
                .all()
            )

            result_dict = [
                {'hour': row.hour.strftime('%H:%M:%S'), 'num_chats': row.num_chats}
                for row in result
            ]

            print(result_dict)

            return {
                "message": "Chats por hora obtenidos exitosamente.",
                "success": True,
                "data": result_dict
            }, 200

        except Exception as e:
            error_dict = {'error': f"Error en la consulta: {str(e)}"}
            return json.dumps({
                "message": "Error al obtener los chats por hora.",
                "success": False,
                "error": error_dict
            }, indent=2), 500
        
    
    def total_of_users():
        try:
            total_users = db.session.query(func.count()).select_from(Users).scalar()

            result_dict = {
                'total_users': total_users,
            }

            print(result_dict)
            return {
                "message": "Datos de usuarios obtenidos exitosamente.",
                "success": True,
                "data": result_dict
            }, 200

        except Exception as e:
            error_dict = {'error': f"Error en la consulta: {str(e)}"}
            return json.dumps({
                "message": "Error al obtener los datos de usuarios.",
                "success": False,
                "error": error_dict
            }, indent=2), 500
