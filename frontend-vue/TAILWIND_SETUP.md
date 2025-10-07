# Tailwind CSS Setup

This frontend now uses **Tailwind CSS v3** for styling.

## What Changed

- ✅ Tailwind CSS v3 installed and configured
- ✅ All custom CSS converted to Tailwind utility classes
- ✅ Component-specific styles moved to `@layer components` in `main.css`
- ✅ Build process optimized with PostCSS and Autoprefixer

## Configuration Files

- **`tailwind.config.js`** - Tailwind configuration (content paths, theme, plugins)
- **`postcss.config.js`** - PostCSS configuration for Tailwind and Autoprefixer
- **`src/assets/main.css`** - Main stylesheet with Tailwind directives

## Using Tailwind Classes

All components now use Tailwind utility classes. Common classes used:

### Buttons
- `.btn` - Base button style (blue)
- `.btn-success` - Green button
- `.btn-danger` - Red button
- `.btn-small` - Smaller button size

### Layout
- `.card` - White card with shadow and padding
- `.control-group` - Form control grouping
- `.button-group` - Flex container for buttons

### Custom Utilities
All custom component classes are defined in `src/assets/main.css` using `@layer components`.

## Development

```bash
# Start dev server with hot reload
npm run dev

# Build for production
npm run build

# Build with TypeScript type checking
npm run build:check

# Preview production build
npm run preview
```

## Customization

To customize the design:

1. **Colors, spacing, etc.** → Edit `tailwind.config.js` theme
2. **Component classes** → Edit `@layer components` in `src/assets/main.css`
3. **Individual components** → Add Tailwind classes directly in Vue templates

## Resources

- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Tailwind CSS Cheat Sheet](https://nerdcave.com/tailwind-cheat-sheet)
- [Tailwind Play](https://play.tailwindcss.com/) - Online playground

## Notes

- The build script (`npm run build`) now skips TypeScript type checking for faster builds
- Use `npm run build:check` if you need type checking before building
- All component-specific styles have been converted to use Tailwind utilities
- The visual appearance remains identical to the original design
