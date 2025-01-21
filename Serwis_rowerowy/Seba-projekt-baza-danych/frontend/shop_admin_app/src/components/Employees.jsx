import React, { useEffect, useState } from 'react';
import CRUDTabView from './CRUD_tabview';

function Employees() {
  const [positions, setPositions] = useState([]);

  useEffect(() => {
    const fetchPositions = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/employee-positions');
        const data = await response.json();
        console.log('Fetched positions:', data); // Debugging line
        setPositions(data);
      } catch (error) {
        console.error('Error fetching positions:', error);
      }
    };

    fetchPositions();
  }, []);

  const validateInput = (selectedItem) => {
    const newErrors = {};
    if (!selectedItem.stanowisko) newErrors.stanowisko = 'Position is required';
    if (!selectedItem.imie) newErrors.imie = 'First name is required';
    if (!selectedItem.nazwisko) newErrors.nazwisko = 'Last name is required';
    if (!selectedItem.wynagrodzenie || isNaN(selectedItem.wynagrodzenie)) {
      newErrors.wynagrodzenie = 'Salary must be a number';
    }
    if (!selectedItem.numer_telefonu || !/^\d{9}$/.test(selectedItem.numer_telefonu)) {
      newErrors.numer_telefonu = 'Phone number must be 9 digits';
    }
    return newErrors;
  };

  const updateItemFields = ['stanowisko', 'imie', 'nazwisko', 'wynagrodzenie', 'numer_telefonu'];
  const addItemFields = ['stanowisko', 'imie', 'nazwisko', 'wynagrodzenie', 'numer_telefonu'];

  return (
    <CRUDTabView
      apiUrl="http://localhost:5000/api/employees"
      itemFields={['stanowisko', 'imie', 'nazwisko', 'wynagrodzenie', 'numer_telefonu']}
      itemIdentifier="id_pracownika"
      fieldLabels={{
        stanowisko: 'Stanowisko',
        imie: 'Imię',
        nazwisko: 'Nazwisko',
        wynagrodzenie: 'Wynagrodzenie',
        numer_telefonu: 'Numer telefonu'
      }}
      validateInput={validateInput}
      title="Pracownicy"
      enableButtons={[true, true]} // Enable both delete and add buttons
      updateItemFields={updateItemFields}
      addItemFields={addItemFields}
      fieldOptions={{
        stanowisko: {
          type: 'combo',
          options: positions.map((position, index) => ({
            value: index,
            label: position
          }))
        }
      }} // Use fetched positions for the stanowisko field
    />
  );
}

export default Employees;