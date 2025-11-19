import { Link, NavLink } from 'react-router-dom';
import { Fragment } from 'react';
import { Disclosure } from '@headlessui/react';
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline';

const links = [
  { label: 'Overview', to: '/' },
  { label: 'Dashboard', to: '/dashboard' },
  { label: 'Research', to: '/#research' },
];

export default function Navbar() {
  return (
    <Disclosure as="nav" className="px-6 md:px-16 py-6 flex items-center justify-between">
      {({ open }) => (
        <Fragment>
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-2xl bg-white/10 flex items-center justify-center border border-white/20">
              <span className="font-display text-xl text-brand-glow">AI</span>
            </div>
            <div>
              <Link to="/" className="font-display text-xl tracking-wide">
                Zenith Expressions
              </Link>
              <p className="text-sm text-white/60 -mt-1">Realtime emotion analytics</p>
            </div>
          </div>

          <div className="hidden md:flex gap-6 items-center">
            {links.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                className={({ isActive }) =>
                  `text-sm uppercase tracking-[0.2em] ${isActive ? 'text-white' : 'text-white/60 hover:text-white'}`
                }
              >
                {link.label}
              </NavLink>
            ))}
            <a
              href="https://github.com/"
              target="_blank"
              rel="noreferrer"
              className="px-5 py-2 rounded-full bg-white text-night font-semibold text-sm tracking-wide"
            >
              GitHub
            </a>
          </div>

          <Disclosure.Button className="md:hidden inline-flex items-center justify-center rounded-md text-white focus:outline-none">
            <span className="sr-only">Open main menu</span>
            {open ? <XMarkIcon className="h-6 w-6" /> : <Bars3Icon className="h-6 w-6" />}
          </Disclosure.Button>

          <Disclosure.Panel className="md:hidden absolute top-20 inset-x-4 bg-card/90 backdrop-blur-xl rounded-3xl border border-white/10 shadow-glass p-6 space-y-4">
            {links.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                className="block text-white/80 uppercase tracking-[0.2em] text-sm"
              >
                {link.label}
              </NavLink>
            ))}
            <a
              href="https://github.com/"
              target="_blank"
              rel="noreferrer"
              className="block text-center py-2 rounded-full bg-white text-night font-semibold text-sm tracking-wide"
            >
              GitHub
            </a>
          </Disclosure.Panel>
        </Fragment>
      )}
    </Disclosure>
  );
}

