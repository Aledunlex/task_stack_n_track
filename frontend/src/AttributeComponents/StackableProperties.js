import React from 'react';

const StackableProperties = ({ stackable_properties }) => (
  <div className='stackable_properties-attribute'>
  <table>
      <thead>
        <tr>
          <th>Property</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        {Object.entries(stackable_properties).map(([key, value]) => (
          <tr key={key}>
            <td>{key}</td>
            <td>{value}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);

export default StackableProperties;

