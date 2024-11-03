const express = require('express');
const mongoose = require('mongoose');
const { body, validationResult } = require('express-validator');
const helmet = require('helmet');
const csurf = require('csurf');
const rateLimit = require('express-rate-limit');
const Product = require('./models/Product');

const app = express();
const port = 3000;

// bdd MongoDB
mongoose.connect('mongodb://localhost:27017/fromagerie', { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log('Connected to MongoDB'))
    .catch(err => console.error('Could not connect to MongoDB', err));

app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use(helmet());
app.use(csurf({ cookie: true }));
app.use(rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 100 
}));

app.get('/', async (req, res) => {
    const products = await Product.find();
    res.render('index', { products });
});

app.get('/products/new', (req, res) => {
    res.render('new', { csrfToken: req.csrfToken() });
});

app.post('/products', [
    body('title').notEmpty().withMessage('Title is required'),
    body('description').notEmpty().withMessage('Description is required'),
    body('price').isFloat({ gt: 0 }).withMessage('Price must be greater than zero')
], (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
    }

    const { title, description, price } = req.body;
    const newProduct = new Product({ title, description, price });
    newProduct.save()
        .then(() => res.redirect('/'))
        .catch(err => res.status(500).json({ error: 'Failed to add product' }));
});

app.get('/form', (req, res) => {
    res.render('form', { csrfToken: req.csrfToken() });
});

app.post('/submit-form', [
    body('email').isEmail().withMessage('Email is invalid'),
    body('password').isLength({ min: 5 }).withMessage('Password must be at least 5 characters long'),
    body('confirmPassword').custom((value, { req }) => value === req.body.password).withMessage('Passwords do not match'),
    body('terms').isBoolean().withMessage('Terms must be accepted'),
    body('captcha').custom((value, { req }) => value === req.body.captcha).withMessage('Captcha is incorrect')
], (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
    }

    console.log(req.body);
    res.send('Form submitted');
});

app.listen(port, () => {
    console.log(`App listening at http://localhost:${port}`);
});

app.get('/', (req, res) => {
    res.render('index', {
      title: 'Home',
      header: 'Welcome to our website!',
      paragraphs: [
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sit amet nulla auctor, vestibulum magna sed, convallis ex.',
        'Cras justo odio, dapibus ac facilisis in, egestas eget quam. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.',
        'Donec id elit non mi porta gravida at eget metus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.'
      ],
      features: [
        { icon: 'fas fa-lock', title: 'Security', description: 'Our website is protected by the latest security measures.' },
        { icon: 'fas fa-speed', title: 'Speed', description: 'Our website is optimized for fast loading times.' },
        { icon: 'fas fa-smile', title: 'Friendly', description: 'Our website is designed to be user-friendly and easy to navigate.' }
      ],
      testimonials: [
        { quote: 'This website is amazing!', author: 'John Doe' },
        { quote: 'I love the design of this website!', author: 'Jane Doe' },
        { quote: 'This website is so fast and secure!', author: 'Bob Smith' }
      ]
    });
  });