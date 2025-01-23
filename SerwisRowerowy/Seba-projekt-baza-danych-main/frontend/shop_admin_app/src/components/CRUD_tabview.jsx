import React, { useEffect, useMemo, useState, useRef, useCallback } from 'react';
import { useTable, useSortBy, useFilters, useResizeColumns, useFlexLayout } from 'react-table';
import './CRUD_tabview.css'; // Import custom CSS
import { fetchItems, handleSaveItem, handleDeleteItems, handleAddItem, handleClosePopup, handleResize, updateContainerPositions, handleMouseDown } from './CRUD_utils';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';



function CRUDTabView({ apiUrl, itemFields, itemIdentifier, fieldLabels, validateInput, title, enableButtons, updateItemFields, addItemFields, fieldOptions, onSearchTermChange }) {
  const [items, setItems] = useState([]);
  const [selectedItem, setSelectedItem] = useState(null);
  const [isMobileView, setIsMobileView] = useState(false);
  const [showPopup, setShowPopup] = useState(false);
  const [errors, setErrors] = useState({});
  const [searchInput, setSearchInput] = useState('');
  const [highlightedRow, setHighlightedRow] = useState(null);
  const [dividerPosition, setDividerPosition] = useState(50); // Initial position in percentage
  const [selectedItems, setSelectedItems] = useState([]);
  const tableContainerRef = useRef(null);
  const searchContainerRef = useRef(null);
  const actionButtonsRef = useRef(null);

  useEffect(() => {
    fetchItems(apiUrl, setItems);
  }, [apiUrl]);

  useEffect(() => {
    const handleResizeWrapper = () => handleResize(setIsMobileView);
    window.addEventListener('resize', handleResizeWrapper);
    handleResizeWrapper();
    return () => window.removeEventListener('resize', handleResizeWrapper);
  }, []);

  useEffect(() => {
    const updateContainerPositionsWrapper = () => updateContainerPositions(tableContainerRef, searchContainerRef, actionButtonsRef);
    updateContainerPositionsWrapper();
    window.addEventListener('resize', updateContainerPositionsWrapper);
    return () => window.removeEventListener('resize', updateContainerPositionsWrapper);
  }, []);

  // Handle item selection
  const handleItemClick = (item) => {
    setSelectedItem(item);
    if (isMobileView) setShowPopup(true);
  };

  // Handle input changes for the selected item
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setSelectedItem((prev) => ({ ...prev, [name]: value }));
  };

  const handleSaveItemWrapper = () => {
    handleSaveItem(selectedItem, validateInput, setErrors, apiUrl, itemIdentifier, setItems, isMobileView, setShowPopup);
  };

  const handleDeleteItemsWrapper = () => {
    handleDeleteItems(selectedItems, apiUrl, itemIdentifier, setItems, setSelectedItems);
  };

  const handleAddItemWrapper = () => {
    handleAddItem(addItemFields, setSelectedItem, setShowPopup);
  };

  const handleClosePopupWrapper = () => {
    handleClosePopup(setSelectedItem, setShowPopup);
  };

  // Table Columns Definition
  const columns = useMemo(
    () => [
      {
        Header: 'Select',
        accessor: 'select',
        disableResizing: true,
        width: 60,
        Cell: ({ row }) => (
          <div className="flex justify-center items-center">
            <input
              type="checkbox"
              onChange={(e) => {
                if (e.target.checked) {
                  setSelectedItems((prev) => [...prev, row.original[itemIdentifier]]);
                } else {
                  setSelectedItems((prev) =>
                    prev.filter((id) => id !== row.original[itemIdentifier])
                  );
                }
              }}
            />
          </div>
        ),
      },
      ...itemFields.map((field) => ({
        Header: fieldLabels[field],
        accessor: field,
      })),
    ],
    [itemFields, fieldLabels, itemIdentifier]
  );

  // Filter data based on search input
  const data = useMemo(
    () =>
      items.filter((item) =>
        itemFields.some((field) =>
          item[field]?.toString().toLowerCase().includes(searchInput.toLowerCase())
        )
      ),
    [items, searchInput, itemFields]
  );

  // React Table Hooks
  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = useTable(
    { columns, data },
    useFilters,
    useSortBy,
    useResizeColumns,
    useFlexLayout
  );

  // Handle divider resizing
  const handleMouseDownWrapper = (e) => {
    handleMouseDown(e, isMobileView, setDividerPosition);
  };

  return (
    <div className="flex flex-col md:flex-row">
      {/* Search and Title Panel */}
      <div
        className="search-container"
        ref={searchContainerRef}
        style={{
          position: 'absolute',
          width: isMobileView ? '100%' : `calc(${dividerPosition}%)`,
          overflow: 'hidden',
          left: '10px',
        }}
      >
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold" style={{ marginRight: '30px' }}>{title}</h2>
          <input
            type="text"
            placeholder="Search..."
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            className="p-2 border rounded"
            style={{ marginRight: '20px' }}
          />
        </div>
      </div>

      {/* Table Panel */}
      <div
        className="table-container"
        ref={tableContainerRef}
        style={{ position: 'absolute', width: isMobileView ? '100%' : `calc(${dividerPosition}% - 10px)`, overflowX: 'auto' }}
      >
        <table {...getTableProps()} className="min-w-full bg-white dark:bg-gray-800">
          <thead>
            {headerGroups.map((headerGroup) => (
              <tr {...headerGroup.getHeaderGroupProps()}>
                {headerGroup.headers.map((column) => (
                  <th
                    {...column.getHeaderProps(column.getSortByToggleProps())}
                    className="py-2 align-middle"
                  >
                    {column.render('Header')}
                    {column.canResize && <div {...column.getResizerProps()} className="resizer" />}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody {...getTableBodyProps()}>
            {rows.map((row) => {
              prepareRow(row);
              return (
                <tr
                  {...row.getRowProps()}
                  className={`border-t ${highlightedRow === row.id ? 'highlighted' : ''}`}
                  onClick={() => handleItemClick(row.original)}
                >
                  {row.cells.map((cell) => (
                    <td {...cell.getCellProps()} className="py-2 cell-content">
                      {cell.render('Cell')}
                    </td>
                  ))}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Divider */}
      {!isMobileView && (
        <div
          className="vertical-divider"
          onMouseDown={(e) => handleMouseDownWrapper(e, isMobileView, setDividerPosition)}
          style={{ left: `${dividerPosition}%` }}
        ></div>
      )}

      {/* New Container */}
      {!isMobileView && (
        <div
          className="edit-add-container"
          style={{
            position: 'absolute',
            width: `calc(100% - ${dividerPosition}% - 10px)`,
            right: '10px',
            overflow: 'hidden',
            top: '0',
          }}
        >
          {/* Content for the new container */}
          <div className="p-4">
          {selectedItem ? (
            <div>
              <h3 className="text-xl font-bold" style={{ paddingBottom: '10px' }}>
                  {selectedItem && selectedItem[itemIdentifier] ? 'Edytuj element' : 'Dodaj element'}
              </h3>

              {(selectedItem[itemIdentifier] ? updateItemFields : addItemFields).map((field) => (
                <div key={field} className="mb-2">
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                    {fieldLabels[field]}
                  </label>
                  {fieldOptions && fieldOptions[field] && fieldOptions[field].type === 'combo' ? (
                    <select
                      name={field}
                      value={selectedItem[field] || ''}
                      onChange={handleInputChange}
                      className="mt-1 p-2 border rounded w-full"
                    >
                      <option value="">{selectedItem[field] || 'Wybierz...'}</option>

                        {fieldOptions[field].options
                        .filter((option) => !selectedItem[field] || selectedItem[field] !== option.value)
                        .map((option) => (
                          <option key={option.value} value={option.value}>
                            {option.label}
                          </option>
                        ))}
                    </select>
                  ) : fieldOptions && fieldOptions[field] && fieldOptions[field].type === 'searchCombo' ? (
                    <div className="flex justify-between space-x-2">
                      <input
                        type="text"
                        name={field}
                        placeholder="Wpisz znak, aby wyszukać..."
                        value={selectedItem[field] || ''}
                        onChange={(e) => {
                          handleInputChange(e);
                          onSearchTermChange(e.target.value);
                        }}
                        className="mt-1 p-2 border rounded w-1/2"
                      />
                      {fieldOptions[field].options
                        .filter(option =>
                          option.searchTerm.toLowerCase().includes((selectedItem[field]?.toString().toLowerCase() || '')))
                        .length > 0 && (
                        <select
                          name={field}
                          value={selectedItem[field] || ''}
                          onChange={handleInputChange}
                          className="mt-1 p-2 border rounded w-1/2"
                        >
                          <option value="">Wybierz...</option>
                          {fieldOptions[field].options
                            .filter(option =>
                              option.searchTerm.toLowerCase().includes((selectedItem[field]?.toString().toLowerCase() || '')))
                            .map((option) => (
                              <option key={option.value} value={option.value}>
                                {option.label}
                              </option>
                            ))}
                        </select>
                      )}
                    </div>
                        )  : fieldOptions && fieldOptions[field] && fieldOptions[field].type === 'dataBox' ? (
                          <DatePicker
                            selected={selectedItem[field] ? new Date(selectedItem[field]) : null}
                            onChange={(date) => handleInputChange({ target: { name: field, value: date.toISOString() } })}
                            dateFormat="dd/MM/yyyy"
                            className="mt-1 p-2 border rounded w-full"
                          />
                        ) : (
                        <input
                          type="text"
                          name={field}
                          value={selectedItem[field] || ''}
                          onChange={handleInputChange}
                          className="mt-1 p-2 border rounded w-full"
                        />
                        )}
                        {errors[field] && (
                        <p className="text-red-500 text-xs mt-1">{errors[field]}</p>
                        )}
                      </div>
                      ))}
                      <button
                      onClick={handleSaveItemWrapper}
                      className="bg-blue-500 text-white px-4 py-2 rounded mt-4"
                      >
                      Zapisz
                      </button>
                    </div>
                    ) : (
                    <p>Wybierz element z tabeli lub utwórz nowy...</p>
                    )}
                  </div>
                  </div>
                  )}

                  {/* Action Buttons at the Bottom */}
      <div
        className="action-buttons bg-gray-700"
        ref={actionButtonsRef}
        style={{
          position: 'absolute',
          bottom: '0',
          width: isMobileView ? '100%' : `calc(${dividerPosition}% - 0px)`,
          padding: '10px',
          left: '0px',
          display: 'flex',
          justifyContent: 'space-between',
          overflow: 'hidden',
        }}
      >
        {enableButtons[0] && (
          <button
            onClick={handleDeleteItemsWrapper}
            className="bg-red-500 text-white px-4 py-2 rounded delete-button"
            disabled={selectedItems.length === 0}
          >
            Usuń zaznaczone
          </button>
        )}
        {enableButtons[1] && (
          <button
            onClick={handleAddItemWrapper}
            className="bg-green-500 text-white px-4 py-2 rounded"
          >
            Dodaj nowy
          </button>
        )}
      </div>

      {/* Popup for Mobile View */}
      {isMobileView && showPopup && (
        <div className="popup-container Mobile">
          {/* Content for the popup */}
          <div className="popup-content">
            <button
              onClick={handleClosePopupWrapper}
              className="absolute top-2 right-2 text-gray-500 hover:text-gray-700"
            >
              X
            </button>
            {selectedItem ? (
            <div>
              <h3 className="text-xl font-bold" style={{ paddingBottom: '10px' }}>
                  {selectedItem && selectedItem[itemIdentifier] ? 'Edytuj element' : 'Dodaj element'}
              </h3>

              {(selectedItem[itemIdentifier] ? updateItemFields : addItemFields).map((field) => (
                <div key={field} className="mb-2">
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                    {fieldLabels[field]}
                  </label>
                  {fieldOptions && fieldOptions[field] && fieldOptions[field].type === 'combo' ? (
                    <select
                      name={field}
                      value={selectedItem[field] || ''}
                      onChange={handleInputChange}
                      className="mt-1 p-2 border rounded w-full"
                    >
                      <option value="">{selectedItem[field] || 'Wybierz...'}</option>

                        {fieldOptions[field].options
                        .filter((option) => !selectedItem[field] || selectedItem[field] !== option.value)
                        .map((option) => (
                          <option key={option.value} value={option.value}>
                            {option.label}
                          </option>
                        ))}
                    </select>
                  ) : fieldOptions && fieldOptions[field] && fieldOptions[field].type === 'searchCombo' ? (
                    <div className="flex justify-between space-x-2">
                      <input
                        type="text"
                        name={field}
                        placeholder="Wpisz znak, aby wyszukać..."
                        value={selectedItem[field] || ''}
                        onChange={(e) => {
                          handleInputChange(e);
                          onSearchTermChange(e.target.value);
                        }}
                        className="mt-1 p-2 border rounded w-1/2"
                      />
                      {fieldOptions[field].options
                        .filter(option =>
                          option.searchTerm.toLowerCase().includes((selectedItem[field]?.toString().toLowerCase() || '')))
                        .length > 0 && (
                        <select
                          name={field}
                          value={selectedItem[field] || ''}
                          onChange={handleInputChange}
                          className="mt-1 p-2 border rounded w-1/2"
                        >
                          <option value="">Wybierz...</option>
                          {fieldOptions[field].options
                            .filter(option =>
                              option.searchTerm.toLowerCase().includes((selectedItem[field]?.toString().toLowerCase() || '')))
                            .map((option) => (
                              <option key={option.value} value={option.value}>
                                {option.label}
                              </option>
                            ))}
                        </select>
                      )}
                    </div>
                        )  : fieldOptions && fieldOptions[field] && fieldOptions[field].type === 'dataBox' ? (
                          <DatePicker
                            selected={selectedItem[field] ? new Date(selectedItem[field]) : null}
                            onChange={(date) => handleInputChange({ target: { name: field, value: date.toISOString() } })}
                            dateFormat="dd/MM/yyyy"
                            className="mt-1 p-2 border rounded w-full"
                          />
                        ) : (
                        <input
                          type="text"
                          name={field}
                          value={selectedItem[field] || ''}
                          onChange={handleInputChange}
                          className="mt-1 p-2 border rounded w-full"
                        />
                        )}
                        {errors[field] && (
                        <p className="text-red-500 text-xs mt-1">{errors[field]}</p>
                        )}
                      </div>
                      ))}
                      <button
                      onClick={handleSaveItemWrapper}
                      className="bg-blue-500 text-white px-4 py-2 rounded mt-4"
                      >
                      Zapisz
                      </button>
                    </div>
                    ) : (
                    <p>Wybierz element z tabeli lub utwórz nowy...</p>
                    )}
          </div>
        </div>
      )}
    </div>
  );
}

export default CRUDTabView;