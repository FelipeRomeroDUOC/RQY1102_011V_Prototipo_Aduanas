import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';
import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

export default function Layout() {
  const { user } = useContext(AuthContext);

  return (
    <div className="flex min-h-screen bg-gray-50">
      {user && <Navbar />}
      <main className={`flex-1 ${user ? 'ml-64' : ''} p-8`}>
        <Outlet />
      </main>
      <footer className="fixed bottom-2 right-4 text-xs text-gray-400">
        v0.2.0-proto · 2026-06-24
      </footer>
    </div>
  );
}
