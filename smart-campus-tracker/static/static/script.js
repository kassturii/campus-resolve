document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("grievanceForm");
  const ticketList = document.getElementById("ticketList");
  const refreshBtn = document.getElementById("refreshBtn");

  async function fetchTickets() {
    try {
      const res = await fetch("/api/grievances");
      const tickets = await res.json();

      if (tickets.length === 0) {
        ticketList.innerHTML = `<p class="subtitle">No grievances lodged yet.</p>`;
        return;
      }

      ticketList.innerHTML = tickets.map(t => {
        let statusClass = "status-pending";
        if (t.status === "In Progress") statusClass = "status-progress";
        if (t.status === "Resolved") statusClass = "status-resolved";

        return `
          <div class="ticket">
            <div class="ticket-top">
              <span class="ticket-id">#TICKET-${t.id} [${t.category}]</span>
              <span class="ticket-status ${statusClass}">${t.status}</span>
            </div>
            <div class="ticket-desc">${t.description}</div>
            <div class="ticket-meta">
              <span>📍 ${t.location} | 👤 ${t.student_name}</span>
            </div>
          </div>
        `;
      }).join('');
    } catch (err) {
      ticketList.innerHTML = `<p style="color: #ef4444;">Failed to load tickets.</p>`;
    }
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const payload = {
      student_name: document.getElementById("student_name").value,
      category: document.getElementById("category").value,
      priority: document.getElementById("priority").value,
      location: document.getElementById("location").value,
      description: document.getElementById("description").value,
    };

    const res = await fetch("/api/grievances", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (res.ok) {
      form.reset();
      fetchTickets();
    } else {
      alert("Error submitting ticket");
    }
  });

  window.changeStatus = async (id, status) => {
    await fetch(`/api/grievances/${id}/status`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status }),
    });
    fetchTickets();
  };

  refreshBtn.addEventListener("click", fetchTickets);
  fetchTickets();
});