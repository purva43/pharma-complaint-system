import { Menu, Moon, Sun } from 'lucide-react';
import { useDispatch, useSelector } from 'react-redux';
import { toggleSidebar, toggleDarkMode } from '../../store/slices/uiSlice';

const Header = () => {
  const dispatch = useDispatch();
  const { sidebarOpen, darkMode } = useSelector((state) => state.ui);

  return (
    <header className="h-16 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between px-6">
      <button
        onClick={() => dispatch(toggleSidebar())}
        className="lg:hidden text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
      >
        <Menu size={24} />
      </button>

      <div className="flex-1" />

      <button
        onClick={() => dispatch(toggleDarkMode())}
        className="p-2 rounded-lg text-gray-500 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-700"
      >
        {darkMode ? <Sun size={20} /> : <Moon size={20} />}
      </button>
    </header>
  );
};

export default Header;
