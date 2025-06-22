import express from 'express';
import User from '../models/User.js';

const router = express.Router();

// Register User
router.post('/register', async (req, res) => {
  try {
    const { name, email, password, organization, role } = req.body;

    // Check if user already exists
    let user = await User.findOne({ email });
    if (user) {
      return res.status(400).json({ msg: 'User already exists' });
    }

    // Create a new user
    user = new User({
      name,
      email,
      password, // Note: Hash the password before saving in production
      organization,
      role,
    });

    await user.save();
    res.status(201).json({ msg: 'User registered successfully' });
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server error');
  }
});

// Login User
router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;

    // Find user by email
    const user = await User.findOne({ email });
    if (!user) {
      return res.status(400).json({ msg: 'Invalid credentials' });
    }

    // Check password
    if (password !== user.password) { // In production, use bcrypt.compare()
      return res.status(400).json({ msg: 'Invalid credentials' });
    }

    // Create token (in production, use JWT)
    const token = 'dummy-token';

    res.json({
      token,
      user: {
        id: user._id,
        name: user.name,
        email: user.email
      }
    });
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server error');
  }
});

export default router;