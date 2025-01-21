import React, { useEffect, useState } from 'react';
import CRUDTabView from './CRUD_tabview';

function Bikes() {
  const [clients, setClients] = useState([]);
  const [filteredClients, setFilteredClients] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchClients = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/clients');
        const data = await response.json();
        setClients(data);
      } catch (error) {
        console.error('Error fetching clients:', error);
      }
    };

    fetchClients();
  }, []);

  useEffect(() => {
    if (searchTerm.length >= 3) {
      const filtered = clients.filter(client =>
        `${client.imie} ${client.nazwisko} (${client.email})`.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredClients(filtered);
    } else {
      setFilteredClients([]);
    }
  }, [searchTerm, clients]);

  const validateInput = (selectedItem) => {
    const newErrors = {};
    if (!selectedItem.typ_roweru) newErrors.typ_roweru = 'Bike type is required';
    if (!selectedItem.marka) newErrors.marka = 'Brand is required';
    if (!selectedItem.model) newErrors.model = 'Model is required';
    if (!selectedItem.klient) newErrors.klient = 'Client is required';
    return newErrors;
  };

  const updateItemFields = ['typ_roweru', 'marka', 'model', 'klient'];
  const addItemFields = ['typ_roweru', 'marka', 'model', 'klient'];

  return (
    <CRUDTabView
      apiUrl="http://localhost:5000/api/bikes"
      itemFields={['typ_roweru', 'marka', 'model', 'klient']}
      itemIdentifier="id_roweru"
      fieldLabels={{
        typ_roweru: 'Typ Roweru',
        marka: 'Marka',
        model: 'Model',
        klient: 'Klient'
      }}
      validateInput={validateInput}
      title="Rowery"
      enableButtons={[true, true]} // Enable both delete and add buttons
      updateItemFields={updateItemFields}
      addItemFields={addItemFields}
      fieldOptions={{
        klient: {
          type: 'searchCombo',
          options: filteredClients.map(client => ({
            value: client.id_klienta,
            label: `${client.imie} ${client.nazwisko} (${client.email})`
          }))
        }
      }}
      onSearchTermChange={setSearchTerm}
    />
  );
}

export default Bikes;