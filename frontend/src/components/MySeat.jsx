import { useEffect, useState } from "react";
import {
  getMyAllocation,
  slideSeat,
  holdSeat,
  withdrawSeat,
} from "../api";

export default function MySeat({ candidateId,refreshKey }) {
  const [seat, setSeat] = useState(null);
  const [msg, setMsg] = useState("");

  useEffect(() => {
    if (!candidateId) return;
    getMyAllocation(candidateId).then(setSeat);
  },[candidateId, refreshKey]);

  if (!candidateId) {
    return (
      <div className="bg-gray-100 p-4 rounded">
        Register to view your seat
      </div>
    );
  }

  if (!seat) {
    return (
      <div className="bg-yellow-100 p-4 rounded">
        No seat allotted yet
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded shadow mt-6">
      <h3 className="text-xl font-bold mb-4">Your Allotted Seat</h3>

      <p><b>Course:</b> {seat.course}</p>
      <p><b>Campus:</b> {seat.campus}</p>
      <p><b>Round:</b> {seat.round}</p>
      <p><b>Status:</b> {seat.seat_status}</p>

      <div className="flex gap-3 mt-4">
        {seat.seat_status === "HELD" && (
          <button
            onClick={async () => {
              const r = await slideSeat(candidateId);
              setMsg(r.message || r.error);
            }}
            className="bg-blue-600 text-white px-4 py-2 rounded"
          >
            Opt for Sliding
          </button>
        )}

        <button
          onClick={async () => {
            const r = await holdSeat(candidateId);
            setMsg(r.message || r.error);
          }}
          className="bg-green-600 text-white px-4 py-2 rounded"
        >
          Hold Seat
        </button>

        <button
          onClick={async () => {
            const r = await withdrawSeat(candidateId);
            setMsg(r.message || r.error);
            setSeat(null);
          }}
          className="bg-red-600 text-white px-4 py-2 rounded"
        >
          Withdraw
        </button>
      </div>

      {msg && <p className="mt-3 text-sm">{msg}</p>}
    </div>
  );
}
