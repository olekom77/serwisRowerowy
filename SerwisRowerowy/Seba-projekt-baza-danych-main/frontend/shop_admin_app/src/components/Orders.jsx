import React, { useEffect, useState } from 'react';
import CRUDTabView from './CRUD_tabview';

function Orders() {
  const [bikes, setBikes] = useState([]);
  const [services, setServices] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [statuses, setStatuses] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [bikesResponse, servicesResponse, employeesResponse, statusesResponse] = await Promise.all([
          fetch('http://localhost:5000/api/bikes'),
          fetch('http://localhost:5000/api/services'),
          fetch('http://localhost:5000/api/employees'),
          fetch('http://localhost:5000/api/order-statuses')
        ]);

        const bikesData = await bikesResponse.json();
        const servicesData = await servicesResponse.json();
        const employeesData = await employeesResponse.json();
        const statusesData = await statusesResponse.json();

        setBikes(bikesData);
        setServices(servicesData);
        setEmployees(employeesData);
        setStatuses(statusesData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const validateInput = (selectedItem) => {
    const newErrors = {};
    if (!selectedItem.id_rowera ||
        isNaN(selectedItem.id_rowera) ||
        !bikes.some(bike => bike.id_rowera === parseInt(selectedItem.id_rowera))) {
      newErrors.id_rowera = 'Valid bike is required';
    }
    if (!selectedItem.data_zlecenia) newErrors.data_zlecenia = 'Order date is required';
    if (!selectedItem.id_uslugi ||
        isNaN(selectedItem.id_uslugi) ||
        !services.some(service => service.id_uslugi === parseInt(selectedItem.id_uslugi))) {
      newErrors.id_uslugi = 'Valid service is required';
    }
    if (!selectedItem.status) newErrors.status = 'Status is required';
    if (!selectedItem.id_pracownika ||
        isNaN(selectedItem.id_pracownika) ||
        !employees.some(employee => employee.id_pracownika === parseInt(selectedItem.id_pracownika))) {
      newErrors.id_pracownika = 'Valid employee is required';
    }
    return newErrors;
  };

  const updateItemFields = ['id_rowera', 'data_zlecenia', 'id_uslugi', 'status', 'id_pracownika'];
  const addItemFields = ['id_rowera', 'data_zlecenia', 'id_uslugi', 'status', 'id_pracownika'];

  return (
    <CRUDTabView
      apiUrl="http://localhost:5000/api/orders"
      itemFields={['marka_typ_roweru', 'nazwa_uslugi', 'klient_imie_nazwisko', 'data_zlecenia', 'status', 'wykonawca_imie_nazwisko', 'id_rowera', 'id_uslugi', 'id_pracownika']}
      itemIdentifier="id_zamowienia"
      fieldLabels={{
        marka_typ_roweru: 'Rower',
        data_zlecenia: 'Data Zlecenia',
        nazwa_uslugi: 'Usługa',
        status: 'Status',
        wykonawca_imie_nazwisko: 'Wykonawca',
        klient_imie_nazwisko: 'Klient',
        id_uslugi: 'ID Usługi',
        id_pracownika: 'ID Pracownika',
        id_rowera: 'ID Roweru'
      }}
      validateInput={validateInput}
      title="Zamówienia"
      enableButtons={[true, true]}
      updateItemFields={updateItemFields}
      addItemFields={addItemFields}
      fieldOptions={{
        id_rowera: {
          type: 'searchCombo',
          options: bikes.map(bike => ({
            value: bike.id_rowera,
            label: `${bike.marka} ${bike.typ_roweru}`,
            searchTerm: `${bike.marka} ${bike.typ_roweru}`.toLowerCase()
          }))
        },
        id_uslugi: {
          type: 'searchCombo',
          options: services.map(service => ({
            value: service.id_uslugi,
            label: service.nazwa,
            searchTerm: service.nazwa.toLowerCase()
          }))
        },
        id_pracownika: {
          type: 'searchCombo',
          options: employees.map(employee => ({
            value: employee.id_pracownika,
            label: `${employee.imie} ${employee.nazwisko}`,
            searchTerm: `${employee.imie} ${employee.nazwisko}`.toLowerCase()
          }))
        },
        status: {
          type: 'combo',
          options: statuses.map((position, index) => ({
            value: position,
            label: position
          }))
        },
        data_zlecenia: {
          type: 'dataBox'
        }
      }}
      onSearchTermChange={setSearchTerm}
    />
  );
}

export default Orders;