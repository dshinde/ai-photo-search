import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import './SearchFilters.css';

function SearchFilters({ onFilter }) {
  const [filters, setFilters] = useState({
    dateRange: [null, null],
    location: '',
    activities: []
  });

  const activityOptions = [
    'standing',
    'sitting',
    'playing',
    'celebrating',
    'eating',
    'traveling'
  ];

  const handleActivityToggle = (activity) => {
    setFilters(prev => ({
      ...prev,
      activities: prev.activities.includes(activity)
        ? prev.activities.filter(a => a !== activity)
        : [...prev.activities, activity]
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onFilter(filters);
  };

  return (
    <div className="search-filters">
      <h3>Advanced Filters</h3>
      <form onSubmit={handleSubmit}>
        <div className="filter-group">
          <label>Date Range</label>
          <DatePicker
            selectsRange
            startDate={filters.dateRange[0]}
            endDate={filters.dateRange[1]}
            onChange={(update) => {
              setFilters(prev => ({ ...prev, dateRange: update }));
            }}
            isClearable
            placeholderText="Select date range"
          />
        </div>
        
        <div className="filter-group">
          <label>Location</label>
          <input 
            type="text" 
            value={filters.location}
            onChange={(e) => setFilters(prev => ({
              ...prev,
              location: e.target.value
            }))}
            placeholder="E.g., Paris, Beach, etc."
          />
        </div>
        
        <div className="filter-group">
          <label>Activities</label>
          <div className="activity-options">
            {activityOptions.map(activity => (
              <button
                key={activity}
                type="button"
                className={`activity-option ${
                  filters.activities.includes(activity) ? 'selected' : ''
                }`}
                onClick={() => handleActivityToggle(activity)}
              >
                {activity}
              </button>
            ))}
          </div>
        </div>
        
        <button type="submit" className="apply-filters">Apply Filters</button>
      </form>
    </div>
  );
}

export default SearchFilters;