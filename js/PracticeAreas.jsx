import React from 'react';

const areas = [
  { icon: 'gavel', title: 'Criminal Defense', description: 'Representation for criminal charges.' },
  { icon: 'balance-scale', title: 'Civil Litigation', description: 'Resolving disputes through litigation.' },
  { icon: 'users', title: 'Family Law', description: 'Guidance for family matters.' },
];

export default function PracticeAreas() {
  return (
    <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      {areas.map(area => (
        <div key={area.title} className="border rounded-lg shadow p-4 bg-white flex flex-col items-center text-center">
          <i className={`fas fa-${area.icon} text-2xl text-gray-700`}></i>
          <h3 className="mt-2 font-serif text-lg font-semibold">{area.title}</h3>
          <p className="mt-1 text-sm text-gray-600">{area.description}</p>
        </div>
      ))}
    </div>
  );
}
