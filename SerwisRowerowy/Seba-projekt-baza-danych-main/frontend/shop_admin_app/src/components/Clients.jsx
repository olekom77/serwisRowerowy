import React from 'react';
import CRUDTabView from './CRUD_tabview';

function Clients() {
  const validateInput = (selectedItem) => {
    const newErrors = {};
    if (!selectedItem.imie) newErrors.imie = 'First name is required';
    if (!selectedItem.nazwisko) newErrors.nazwisko = 'Last name is required';
    if (!selectedItem.numer_telefonu || !/^\d{9}$/.test(selectedItem.numer_telefonu)) {
      newErrors.numer_telefonu = 'Phone number must be 9 digits';
    }
    if (!selectedItem.email || !/\S+@\S+\.\S+/.test(selectedItem.email)) {
      newErrors.email = 'Invalid email address';
    }
    return newErrors;
  };

  const updateItemFields = ['imie', 'nazwisko', 'numer_telefonu', 'email'];
  const addItemFields = ['imie', 'nazwisko', 'numer_telefonu', 'email'];

  return (
    <CRUDTabView
      apiUrl="http://localhost:5000/api/clients"
      itemFields={['imie', 'nazwisko', 'numer_telefonu', 'email']}
      itemIdentifier="id_klienta"
      fieldLabels={{
        imie: 'Imię',
        nazwisko: 'Nazwisko',
        numer_telefonu: 'Numer telefonu',
        email: 'Email'
      }}
      validateInput={validateInput}
      title="Klienci"
      enableButtons={[true, true]}
      updateItemFields={updateItemFields}
      addItemFields={addItemFields}
      fieldOptions={{}} // No specific field options for clients
    />
  );
}

export default Clients;