import { useEffect, useState } from "react";
import { getAllocations } from "../api";

export default function AllocationResult({ candidateId }) {
  const [allocation, setAllocation] = useState(null);

  useEffect(() => {
    if (!candidateId) return;

    const load = async () => {
      const all = await getAllocations();
      const mine = all.find(
        (a) => String(a.candidate_id) === String(candidateId)
      );
      setAllocation(mine || null);
    };

    load();
  }, [candidateId]);

  if (!candidateId) return null;

  if (!allocation) {
    return (
      <div className="bg-yellow-100 p-4 rounded mt-4">
        No seat allocated yet
      </div>
    );
  }

  return (
    <div className="bg-green-100 p-6 rounded shadow mt-6">
      <h3 className="text-xl font-bold mb-4">Your Allocation</h3>

      <div><b>Course:</b> {allocation.course}</div>
      <div><b>Campus:</b> {allocation.campus}</div>
      <div><b>Round:</b> {allocation.round}</div>
      <div><b>Status:</b> {allocation.seat_status}</div>
    </div>
  );
}
