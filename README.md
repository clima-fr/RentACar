# Rent a Car
>This project was developed for CESAE's AWS Re/Start course. Python programming module. 

The project aims to implement an operational management system for a Rent-a-car. Following these instructions:

1. The rent-a-car company has a fleet of cars represented by the listAutomovel. This should store dictionaries with the following keys: id, matricula, marca, modelo, cor, portas, precoDiario, cilindrada, potencia;
2. The company's clients should be registered in the listClient. This list should store dictionaries with the following keys: id, nome, nif, dataNascimento, telefone, email. 
Note: phone and email must be unique;
3. Reservations should be recorded in the listBooking list. This should store dictionaries with the keys: data_inicio, data_fim, cliente_id, automovel_id, precoReserva, numeroDias;
4. Each list must be loaded with data from JSON files: listcliente.json, listautomovel.json and
listbooking.json;
5. Manage the 3 lists. The program should allow you to list, add, update and remove;
6. Customers can benefit from discounts depending on the total number of days of the rental: until 4 days 0%, 5 to 8 days 15%, more than 8 days 25%;
7. List of future bookings;
8. Search for a car using "matricula" as a parameter. And a list of the last 5 rentals;
9. Search for a client using "nif" as a parameter. And a list of the last 5 rentals;
10. Add a functional menu to the program that clearly identifies each feature. (We chose Cutie)

## Contributors

>I would like to extend my deepest gratitude to my group for the remarkable partnership:

* Pedro Matos (https://github.com/PedroMatosMartins)
* Pedro Pinto (https://github.com/PedroNeivaPinto)
* Temaco Mafumba (https://github.com/temaco)
