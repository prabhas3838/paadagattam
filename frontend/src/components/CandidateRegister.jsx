import { useState } from "react";
import { registerCandidate } from "../api";

export default function CandidateRegister({ onRegistered }) {
  const [candidateId, setCandidateId] = useState("");
  const [rank, setRank] = useState("");
  const [msg, setMsg] = useState("");

  const register = async () => {
    if (!candidateId || !rank) {
      setMsg("Candidate ID and Rank required");
      return;
    }

    const res = await registerCandidate(candidateId, rank);

    if (res.id || res.candidate_id) {
      setMsg("Candidate registered successfully ✅");
      onRegistered(candidateId);
    } else {
      setMsg(res.error || "Registration failed");
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-xl font-semibold mb-4">Candidate Registration</h3>

      <input
        className="w-full p-2 border rounded mb-3"
        placeholder="Candidate ID (e.g. 100)"
        value={candidateId}
        onChange={(e) => setCandidateId(e.target.value)}
      />

      <input
        className="w-full p-2 border rounded mb-3"
        placeholder="AEEE Rank"
        type="number"
        value={rank}
        onChange={(e) => setRank(e.target.value)}
      />

      <button
        onClick={register}
        className="bg-blue-600 text-white px-4 py-2 rounded"
      >
        Register
      </button>

      {msg && <p className="mt-3 text-sm">{msg}</p>}
    </div>
  );
}
