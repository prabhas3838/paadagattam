import { useEffect, useState } from "react";
import { getOptions } from "../api";

export default function SeatBox() {
  const [seats, setSeats] = useState([]);

  useEffect(() => {
    getOptions().then(setSeats);
  }, []);

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-xl font-semibold mb-4">Available Seats</h3>
      {seats.map((s, i) => (
        <div key={i} className="flex justify-between border-b py-2">
          <span>{s.course} – {s.campus}</span>
          <span className="font-bold">{s.remaining_seats}</span>
        </div>
      ))}
    </div>
  );
}
