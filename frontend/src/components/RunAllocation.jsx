import { runAllocation, getAllocations } from "../api";

export default function RunAllocation({ roundNo, onDone }) {
  const handleRun = async () => {
    const res = await runAllocation(roundNo);

    if (res.error) {
      alert(res.error);
      return;
    }

    const all = await getAllocations();
    onDone(all);   // 🔥 THIS WAS MISSING
    alert(res.message);
  };

  return (
    <button
      onClick={handleRun}
      className="bg-red-600 text-white px-6 py-2 rounded mt-4"
    >
      Run Allocation for Round {roundNo}
    </button>
  );
}
