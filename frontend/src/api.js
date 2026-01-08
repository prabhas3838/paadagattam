const BASE_URL = "http://localhost:8000";

export const getRoundStatus = (roundNo) =>
  fetch(`${BASE_URL}/round/${roundNo}/status`).then((r) => r.json());



  export async function getOptions() {
    const res = await fetch(`${BASE_URL}/options`);
    if (!res.ok) {
      throw new Error("Failed to fetch options");
    }
    return res.json();
  }
  
  export const getPreferences = (candidateId) =>
  fetch(`${BASE_URL}/candidate/${candidateId}/preferences`)
    .then((r) => r.json());


export const addPreference = (candidateId, pref) =>
  fetch(`${BASE_URL}/candidate/${candidateId}/preference`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(pref),
  });

export const submitPreferences = (candidateId) =>
  fetch(`${BASE_URL}/candidate/${candidateId}/submit`, {
    method: "POST",
  });


  export const runAllocation = (roundNo) =>
  fetch(`${BASE_URL}/allocate/round/${roundNo}`, {
    method: "POST",
  }).then((r) => r.json());

export const getAllocations = () =>
  fetch(`${BASE_URL}/allocations`).then((r) => r.json());

  export const registerCandidate = async (candidateId, rank) => {
    const res = await fetch("http://localhost:8000/candidate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        candidate_id: candidateId,
        aeee_rank: Number(rank),
      }),
    });
  
    return res.json();
  };
  
  export const getMyAllocation = async (candidateId) => {
    const res = await fetch(`${BASE_URL}/candidate/${candidateId}/allocation`);
    if (!res.ok) return null;
  
    const allocation = await res.json();
    return allocation; // <-- IT IS ALREADY THE OBJECT
  };
  
  
  export const slideSeat = (candidateId) =>
    fetch(`${BASE_URL}/candidate/${candidateId}/slide`, {
      method: "POST",
    }).then(r => r.json());
  
  export const holdSeat = (candidateId) =>
    fetch(`${BASE_URL}/candidate/${candidateId}/hold`, {
      method: "POST",
    }).then(r => r.json());
  
  export const withdrawSeat = (candidateId) =>
    fetch(`${BASE_URL}/candidate/${candidateId}/withdraw`, {
      method: "POST",
    }).then(r => r.json());
  