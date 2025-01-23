import React from 'react';
import CRUDTabView from './CRUD_tabview';

function Services() {
  const validateInput = (selectedItem) => {
    const newErrors = {};
    if (!selectedItem.nazwa) newErrors.nazwa = 'Name is required';
    if (!selectedItem.opis) newErrors.opis = 'Description is required';
    if (!selectedItem.cena || isNaN(selectedItem.cena)) {
      newErrors.cena = 'Price must be a number';
    }
    return newErrors;
  };

  const updateItemFields = ['nazwa', 'opis', 'cena'];
  const addItemFields = ['nazwa', 'opis', 'cena'];

  return (
    <CRUDTabView
      apiUrl="http://localhost:5000/api/services"
      itemFields={['nazwa', 'opis', 'cena']}
      itemIdentifier="id_uslugi"
      fieldLabels={{
        nazwa: 'Nazwa',
        opis: 'Opis',
        cena: 'Cena'
      }}
      validateInput={validateInput}
      title="Usługi"
      enableButtons={[true, true]} // Enable both delete and add buttons
      updateItemFields={updateItemFields}
      addItemFields={addItemFields}
      fieldOptions={{}} // No specific field options for services
    />
  );
}

export default Services;