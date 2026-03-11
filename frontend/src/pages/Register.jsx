import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { authAPI } from '../utils/api';
import { FaUser, FaEnvelope, FaPhone, FaLock, FaMapMarkerAlt, FaTractor } from 'react-icons/fa';



const Register = ({ setUser }) => {
    const { t, language } = useLanguage();
    const navigate = useNavigate();

    // Get districts based on current language
    const districtList = t('districts');

    const [formData, setFormData] = useState({
        name: '',
        email: '',
        phone: '',
        password: '',
        district: '',
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const response = await authAPI.register(formData);
            setUser(response.data);
            navigate('/form');
        } catch (err) {
            setError(err.response?.data?.error || 'Registration failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex flex-col items-center justify-center p-4 py-12">
            {/* Project Branding */}
            <div className="text-center mb-8 animate-fade-in">
                <h1 className="text-4xl font-bold text-farm-green-700 flex items-center justify-center gap-2 mb-2">
                    {t('appName')}
                </h1>
                <p className="text-sm text-gray-500 font-semibold tracking-wider uppercase">
                    {t('appSubtitle')}
                </p>
            </div>

            <div className="card max-w-2xl w-full animate-fade-in">
                {/* Logo/Icon */}
                <div className="text-center mb-8">
                    <div className="icon-container bg-farm-green-100 text-farm-green-600 mx-auto mb-4">
                        <FaTractor />
                    </div>
                    <h2 className="text-2xl font-bold text-farm-green-800">
                        {t('register')}
                    </h2>
                </div>

                {error && (
                    <div className="bg-red-100 border-2 border-red-400 text-red-700 px-4 py-3 rounded-lg mb-4">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-6">
                    {/* Name */}
                    <div>
                        <label className="block text-lg font-semibold text-gray-700 mb-2">
                            <FaUser className="inline mr-2" />
                            {t('name')} *
                        </label>
                        <input
                            type="text"
                            name="name"
                            value={formData.name}
                            onChange={handleChange}
                            className="input-field"
                            required
                            placeholder={t('name')}
                        />
                    </div>

                    {/* Email */}
                    <div>
                        <label className="block text-lg font-semibold text-gray-700 mb-2">
                            <FaEnvelope className="inline mr-2" />
                            {t('email')}
                        </label>
                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            className="input-field"
                            placeholder="farmer@example.com"
                        />
                    </div>

                    {/* Phone */}
                    <div>
                        <label className="block text-lg font-semibold text-gray-700 mb-2">
                            <FaPhone className="inline mr-2" />
                            {t('phone')}
                        </label>
                        <input
                            type="tel"
                            name="phone"
                            value={formData.phone}
                            onChange={handleChange}
                            className="input-field"
                            placeholder="9876543210"
                        />
                    </div>

                    {/* District */}
                    <div>
                        <label className="block text-lg font-semibold text-gray-700 mb-2">
                            <FaMapMarkerAlt className="inline mr-2" />
                            {t('district')} *
                        </label>
                        <select
                            name="district"
                            value={formData.district}
                            onChange={handleChange}
                            className="input-field"
                            required
                        >
                            <option value="">{t('selectDistrict')}</option>
                            {Array.isArray(districtList) && districtList.map(district => (
                                <option key={district} value={district}>{district}</option>
                            ))}
                        </select>
                    </div>

                    {/* Password */}
                    <div>
                        <label className="block text-lg font-semibold text-gray-700 mb-2">
                            <FaLock className="inline mr-2" />
                            {t('password')} *
                        </label>
                        <input
                            type="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            className="input-field"
                            required
                            placeholder="••••••••"
                            minLength="6"
                        />
                    </div>

                    {/* Submit Button */}
                    <button
                        type="submit"
                        disabled={loading}
                        className="btn-primary w-full"
                    >
                        {loading ? '...' : t('register')}
                    </button>
                </form>

                {/* Login Link */}
                <div className="mt-6 text-center">
                    <p className="text-gray-600">
                        {t('alreadyHaveAccount')}{' '}
                        <Link to="/login" className="text-farm-green-600 font-semibold hover:underline">
                            {t('login')}
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Register;
