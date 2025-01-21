export const fetchItems = async (apiUrl, setItems) => {
    try {
      const response = await fetch(apiUrl);
      const data = await response.json();
      setItems(data);
    } catch (error) {
      console.error('Error fetching items:', error);
    }
  };

  export const handleSaveItem = async (selectedItem, validateInput, setErrors, apiUrl, itemIdentifier, setItems, isMobileView, setShowPopup) => {
    const validationErrors = validateInput(selectedItem);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    try {
      const method = selectedItem[itemIdentifier] ? 'PUT' : 'POST';
      const url = selectedItem[itemIdentifier] ? `${apiUrl}/${selectedItem[itemIdentifier]}` : apiUrl;
      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(selectedItem),
      });
      const savedItem = await response.json();

      if (method === 'POST') {
        setItems((prev) => [...prev, savedItem]);
      } else {
        setItems((prev) =>
          prev.map((item) =>
            item[itemIdentifier] === savedItem[itemIdentifier] ? savedItem : item
          )
        );
      }

      if (isMobileView) setShowPopup(false);
      window.location.reload(); // Refresh the page
    } catch (error) {
      console.error('Error saving item:', error);
    }
  };

  export const handleDeleteItems = async (selectedItems, apiUrl, itemIdentifier, setItems, setSelectedItems) => {
    for (const itemId of selectedItems) {
      try {
        await fetch(`${apiUrl}/${itemId}`, { method: 'DELETE' });
        setItems((prev) => prev.filter((item) => item[itemIdentifier] !== itemId));
      } catch (error) {
        console.error('Error deleting item:', error);
      }
    }
    setSelectedItems([]);
    window.location.reload(); // Refresh the page
  };

  export const handleAddItem = (addItemFields, setSelectedItem, setShowPopup) => {
    const newItem = addItemFields.reduce((acc, field) => {
      acc[field] = '';
      return acc;
    }, {});
    setSelectedItem(newItem);
    setShowPopup(true);
  };

  export const handleClosePopup = (setSelectedItem, setShowPopup) => {
    setSelectedItem(null);
    setShowPopup(false);
  };

  export const handleResize = (setIsMobileView) => {
    setIsMobileView(window.innerWidth <= 768);
  };

  export const updateContainerPositions = (tableContainerRef, searchContainerRef, actionButtonsRef) => {
    const header = document.querySelector('header');
    const tableContainer = tableContainerRef.current;
    const searchContainer = searchContainerRef.current;
    const editAddContainer = document.querySelector('.edit-add-container');
    const actionButtons = actionButtonsRef.current;

    if (header && tableContainer && searchContainer && actionButtons) {
      const headerHeight = header.offsetHeight;
      const searchHeight = searchContainer.offsetHeight;
      const actionButtonsHeight = actionButtons.offsetHeight;
      searchContainer.style.top = (headerHeight + 15) + 'px';
      tableContainer.style.top = (headerHeight + searchHeight + 10) + 'px';
      tableContainer.style.maxHeight = `calc(100vh - ${headerHeight + searchHeight + actionButtonsHeight + 30}px)`;
      editAddContainer.style.top = (headerHeight + 15) + 'px';
      editAddContainer.style.maxHeight = `calc(100vh - ${headerHeight}px)`;
    }
  };

  export const handleMouseDown = (e, isMobileView, setDividerPosition) => {
    if (isMobileView) return; // Disable divider in mobile view

    const startX = e.clientX;

    const handleMouseMove = (e) => {
      const newDividerPosition = Math.min(90, Math.max(10, (e.clientX / window.innerWidth) * 100));
      setDividerPosition(newDividerPosition);
    };

    const handleMouseUp = () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
      document.body.style.userSelect = ''; // Re-enable text selection
    };

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
    document.body.style.userSelect = 'none'; // Disable text selection
  };