import { useEffect, useState } from "react";
import { getRoundStatus } from "../api";

export default function RoundStatus({ roundNo }) {
  const [status, setStatus] = useState(null);

  useEffect(() => {
    const id = setInterval(async () => {
      setStatus(await getRoundStatus(roundNo));
    }, 1000);
    return () => clearInterval(id);
  }, [roundNo]);

  if (!status) return null;

  const color =
    status.status === "OPEN"
      ? "bg-green-100 text-green-800"
      : status.status === "CLOSED"
      ? "bg-red-100 text-red-800"
      : "bg-yellow-100 text-yellow-800";

  return (
    <div className={`p-4 rounded-lg ${color}`}>
      <h2 className="font-semibold text-lg">Round {roundNo}</h2>
      <p>Status: <b>{status.status}</b></p>
      {status.seconds_remaining && (
        <p>⏳ {status.seconds_remaining} seconds remaining</p>
      )}
    </div>
  );
}
