import { useState } from "react";

type User = {
  id: number;
  firstName: string;
  lastName: string;
};

const users: User[] = [
  { id: 1, firstName: "Jan", lastName: "Novák" },
  { id: 2, firstName: "Jana", lastName: "Nováková" },
  { id: 3, firstName: "Petr", lastName: "Černý" },
  { id: 4, firstName: "David", lastName: "Čech" },
];

export default function App() {
  const [rawSearch, setSearch] = useState("");

  const search = rawSearch.trim().toLowerCase();

  const filteredUsers = !search
    ? users
    : users.filter((user) => {
        return (
          user.firstName.toLowerCase().includes(search) ||
          user.lastName.toLowerCase().includes(search)
        );
      });

  return (
    <>
      <h1>Uživatelé</h1>

      <input
        type="text"
        placeholder="Vyhledat"
        value={rawSearch}
        onChange={(e) => setSearch(e.target.value)}
      />

      <ul>
        {filteredUsers.map((user) => (
          <li key={user.id}>
            {user.firstName} {user.lastName}
          </li>
        ))}
      </ul>
    </>
  );
}
