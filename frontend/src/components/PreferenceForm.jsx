import { useEffect, useState } from "react";
import { addPreference, submitPreferences, getPreferences } from "../api";

export default function PreferenceForm({ candidateId }) {
  const [form, setForm] = useState({
    course: "",
    campus: "",
    priority: "",
  });

  const [preferences, setPreferences] = useState([]);

  const loadPreferences = async () => {
    if (!candidateId) return;
    const data = await getPreferences(candidateId);
    setPreferences(data || []);
  };

  useEffect(() => {
    loadPreferences();
  }, [candidateId]);

  if (!candidateId) {
    return (
      <div className="bg-gray-100 p-6 rounded">
        Register candidate to add preferences
      </div>
    );
  }

  const update = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const addPref = async () => {
    await addPreference(candidateId, {
      course: form.course,
      campus: form.campus,
      priority: Number(form.priority),
    });

    setForm({ course: "", campus: "", priority: "" });
    loadPreferences(); // 🔥 refresh list
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-xl font-semibold mb-4">
        Preferences (Candidate {candidateId})
      </h3>

      {/* ADD FORM */}
      {["course", "campus", "priority"].map((f) => (
        <input
          key={f}
          name={f}
          value={form[f]}
          placeholder={f.toUpperCase()}
          className="w-full p-2 border rounded mb-2"
          onChange={update}
        />
      ))}

      <div className="flex gap-3 mb-4">
        <button
          className="bg-blue-600 text-white px-4 py-2 rounded"
          onClick={addPref}
        >
          Add Preference
        </button>

        <button
          className="bg-green-600 text-white px-4 py-2 rounded"
          onClick={() => submitPreferences(candidateId)}
        >
          Submit
        </button>
      </div>

      {/* SHOW PREFERENCES */}
      <div className="mt-4">
        <h4 className="font-semibold mb-2">Saved Preferences</h4>

        {preferences.length === 0 && (
          <p className="text-sm text-gray-500">No preferences added</p>
        )}

        {preferences
          .sort((a, b) => a.priority - b.priority)
          .map((p, i) => (
            <div
              key={i}
              className="flex justify-between border-b py-1 text-sm"
            >
              <span>
                {p.priority}. {p.course} – {p.campus}
              </span>
            </div>
          ))}
      </div>
    </div>
  );
}
