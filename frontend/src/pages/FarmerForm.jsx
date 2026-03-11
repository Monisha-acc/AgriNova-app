import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { farmerAPI } from '../utils/api';
import {
    FaUser, FaLandmark, FaMicrochip, FaUniversity, FaMoneyBill, FaHeart,
    FaArrowRight, FaArrowLeft, FaCheck
} from 'react-icons/fa';

const FarmerForm = ({ user }) => {
    const { t, language } = useLanguage();
    const navigate = useNavigate();
    const [currentStep, setCurrentStep] = useState(1);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const [formData, setFormData] = useState({
        // Step 1: Basic Profile
        age: '',
        gender: '',
        education: '',
        experience: '',
        income: '',
        household_size: '',
        physically_challenged: false,

        // Step 2: Land & Crop
        land_area: '',
        land_ownership: '',
        crops: [],
        soil_type: '',
        irrigation_source: '',
        water_availability: '',
        yield_history: '',
        market_linkage: '',

        // Step 3: Technology Usage
        technologies_used: [],
        other_technology: '',

        // Step 4: Scheme Awareness
        schemes_aware: [],
        other_scheme: '',
        amma_two_wheeler_aware: false,
        tn_micro_irrigation_aware: false,
        tn_free_electricity_aware: false,
        kalaignar_scheme_aware: false,
        tn_soil_health_aware: false,
        tn_farm_mechanization_aware: false,

        // Step 5: Financial Behaviour
        has_loan: false,
        has_insurance: false,
        savings_habit: '',
        risk_level: '',

        // Step 6: Tech Attitude
        openness: 3,
        trust: 3,
        peer_influence: 3,
        govt_influence: 3,

        // Step 7: Region & Social
        block: '',
        taluk: '',
        village: '',
        agro_climatic_zone: '',
        farmer_category: '',
        farmer_smart_card: false,

        // Step 8: Water & Energy
        borewell_depth: '',
        water_scarcity_months: '',
        three_phase_power: false,
        power_hours_per_day: '',

        // Step 9: Market & Training
        selling_uzhavar_sandhai: false,
        using_enam: false,
        market_type: '',
        attended_training: false,
        met_vao_aeo: false,
        visited_tnau_farm: false,
        read_tamil: false,
        read_english: false,
        voice_guidance_pref: false,
        using_uzhavan_app: false,
        watch_agri_youtube: false,
        in_whatsapp_groups: false,

        // Other details
        other_education: '',
        other_crops: '',
        other_soil_type: '',
        other_irrigation_source: '',
        other_water_availability: '',
        other_yield_history: '',
        other_savings_habit: '',
        other_risk_level: '',
        other_agro_climatic_zone: '',
        other_farmer_category: '',
        other_market_type: '',
        other_gender: '',
        other_land_ownership: '',

        // Extended Financial & Risk Behaviour
        loan_source: '',
        repay_on_time: false,
        enrolled_pmfby: false,
        crop_loss_earlier: false,
        farming_only_income: false,
        has_other_income: false,
        save_after_harvest: false,
        saving_location: '',
        invested_equipment: false,
        digital_payment_usage: false,
        check_market_price: false,
        risk_try_new_methods: 3,
        risk_afraid_loss: 3,
        risk_follow_neighbors: 3,
    });

    const totalSteps = 7;

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData({
            ...formData,
            [name]: type === 'checkbox' ? checked : value,
        });
    };

    const handleCheckboxArray = (name, value) => {
        const currentArray = formData[name];
        if (currentArray.includes(value)) {
            setFormData({
                ...formData,
                [name]: currentArray.filter(item => item !== value),
            });
        } else {
            setFormData({
                ...formData,
                [name]: [...currentArray, value],
            });
        }
    };

    const handleSlider = (name, value) => {
        setFormData({
            ...formData,
            [name]: parseInt(value),
        });
    };

    const nextStep = () => {
        if (currentStep < totalSteps) {
            setCurrentStep(currentStep + 1);
            window.scrollTo(0, 0);
        }
    };

    const prevStep = () => {
        if (currentStep > 1) {
            setCurrentStep(currentStep - 1);
            window.scrollTo(0, 0);
        }
    };

    const handleSubmit = async () => {
        setError('');
        setLoading(true);

        try {
            await farmerAPI.submitData(formData);
            navigate('/dashboard');
        } catch (err) {
            setError(err.response?.data?.error || 'Submission failed');
            setLoading(false);
        }
    };

    const renderProgressBar = () => {
        const progress = (currentStep / totalSteps) * 100;
        return (
            <div className="mb-8">
                <div className="flex justify-between mb-2">
                    <span className="text-sm font-semibold text-gray-700">
                        Step {currentStep} of {totalSteps}
                    </span>
                    <span className="text-sm font-semibold text-farm-green-600">
                        {Math.round(progress)}%
                    </span>
                </div>
                <div className="progress-bar">
                    <div
                        className="progress-fill bg-farm-green-600"
                        style={{ width: `${progress}%` }}
                    />
                </div>
            </div>
        );
    };

    const renderStep1 = () => (
        <div className="space-y-6 animate-fade-in">
            <div className="text-center mb-6">
                <div className="icon-container bg-farm-green-100 text-farm-green-600 mx-auto mb-3">
                    <FaUser />
                </div>
                <h2 className="text-2xl font-bold text-farm-green-800">{t('step1')}</h2>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
                <div>
                    <label className="block text-lg font-semibold text-gray-700 mb-2">{t('age')}</label>
                    <input type="number" name="age" value={formData.age} onChange={handleChange}
                        className="input-field" required placeholder={t('agePlaceholder')} />
                </div>

                <div>
                    <label className="block text-lg font-semibold text-gray-700 mb-2">{t('gender')}</label>
                    <select name="gender" value={formData.gender} onChange={handleChange} className="input-field" required>
                        <option value="">{t('selectOption')}</option>
                        <option value="Male">Male / ஆண்</option>
                        <option value="Female">Female / பெண்</option>
                        <option value="Other">Other / பிற</option>
                    </select>
                </div>

                {formData.gender === 'Other' && (
                    <div className="animate-fade-in">
                        <label className="block text-lg font-semibold text-gray-700 mb-2">{t('specifyOther')}</label>
                        <input type="text" name="other_gender" value={formData.other_gender} onChange={handleChange}
                            className="input-field" placeholder="Enter gender details" />
                    </div>
                )}

                <div>
                    <label className="block text-lg font-semibold text-gray-700 mb-2">{t('education')}</label>
                    <select name="education" value={formData.education} onChange={handleChange} className="input-field" required>
                        <option value="">{t('selectOption')}</option>
                        <option value="No Formal">{t('eduNoFormal')}</option>
                        <option value="Primary">{t('eduPrimary')}</option>
                        <option value="Middle">{t('eduMiddle')}</option>
                        <option value="High">{t('eduHigh')}</option>
                        <option value="Higher Secondary">{t('eduHigherSecondary')}</option>
                        <option value="Diploma">{t('eduDiploma')}</option>
                        <option value="Degree">{t('eduDegree')}</option>
                        <option value="Postgraduate">{t('eduPostgraduate')}</option>
                        <option value="Other">{t('others')}</option>
                    </select>
                </div>

                {formData.education === 'Other' && (
                    <div className="animate-fade-in">
                        <label className="block text-lg font-semibold text-gray-700 mb-2">{t('specifyOther')}</label>
                        <input type="text" name="other_education" value={formData.other_education} onChange={handleChange}
                            className="input-field" placeholder="Enter education details" />
                    </div>
                )}

                <div>
                    <label className="block text-lg font-semibold text-gray-700 mb-2">{t('experience')}</label>
                    <input type="number" name="experience" value={formData.experience} onChange={handleChange}
                        className="input-field" required placeholder="Years" />
                </div>

                <div>
                    <label className="block text-lg font-semibold text-gray-700 mb-2">{t('income')}</label>
                    <select name="income" value={formData.income} onChange={handleChange} className="input-field" required>
                        <option value="">{t('selectOption')}</option>
                        <option value="Below 50000">{t('incomeBelow50k')}</option>
                        <option value="50000-100000">{t('income50k_100k')}</option>
                        <option value="100000-200000">{t('income100k_200k')}</option>
                        <option value="200000-500000">{t('income200k_500k')}</option>
                        <option value="Above 500000">{t('incomeAbove500k')}</option>
                    </select>
                </div>

                <div>
                    <label className="block text-lg font-semibold text-gray-700 mb-2">{t('householdSize')}</label>
                    <input type="number" name="household_size" value={formData.household_size} onChange={handleChange}
                        className="input-field" required />
                </div>

                <div className="flex items-center space-x-4 p-4 bg-farm-green-50 border-2 border-farm-green-200 rounded-lg">
                    <input
                        type="checkbox"
                        name="physically_challenged"
                        id="physically_challenged"
                        checked={formData.physically_challenged}
                        onChange={handleChange}
                        className="w-6 h-6 text-farm-green-600 rounded focus:ring-farm-green-500"
                    />
                    <label htmlFor="physically_challenged" className="text-lg font-semibold text-farm-green-800">
                        {t('physicallyChallenged')}
                    </label>
                </div>
            </div>
        </div>
    );

    const renderStep2 = () => (
        <div className="space-y-6 animate-fade-in">
            <div className="text-center mb-6">
                <div className="icon-container bg-farm-brown-100 text-farm-brown-600 mx-auto mb-3">
                    <FaLandmark />
                </div>
                <h2 className="text-2xl font-bold text-farm-green-800">{t('step2')}</h2>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
                <div>
                    <label className="block text-lg font-semibold text-gray-700 mb-2">{t('landArea')}</label>
                    <input type="number" step="0.1" name="land_area" value={formData.land_area} onChange={handleChange}
                        className="input-field" required placeholder={t('landAreaPlaceholder')} />
                </div>

                <div>
                    <label className="block text-lg font-semibold text-gray-700 mb-2">{t('landOwnership')}</label>
                    <select name="land_ownership" value={formData.land_ownership} onChange={handleChange} className="input-field" required>
                        <option value="">{t('selectOption')}</option>
                        <option value="Owned">{t('landOwned')}</option>
                        <option value="Leased">{t('landLeased')}</option>
                        <option value="Rented">{t('landRented')}</option>
                        <option value="Sharecropping">{t('landSharecropping')}</option>
                        <option value="Family">{t('landFamily')}</option>
                        <option value="Govt">{t('landGovt')}</option>
                        <option value="Temple">{t('landTemple')}</option>
                        <option value="Informal">{t('landInformal')}</option>
                        <option value="Other">Other / பிற</option>
                    </select>
                </div>

                {formData.land_ownership === 'Other' && (
                    <div className="animate-fade-in">
                        <label className="block text-lg font-semibold text-gray-700 mb-2">{t('specifyOther')}</label>
                        <input type="text" name="other_land_ownership" value={formData.other_land_ownership} onChange={handleChange}
                            className="input-field" placeholder="Enter ownership details" />
                    </div>
                )}

                <div className="md:col-span-2">
                    <label className="block text-lg font-semibold text-gray-700 mb-2">{t('cropPattern')} (Select all that apply / பொருந்தும் அனைத்தையும் தேர்ந்தெடுக்கவும்)</label>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-3 bg-white p-4 border-2 border-gray-200 rounded-lg">
                        {[
                            { id: 'Paddy', label: 'cropPaddy' },
                            { id: 'Sugarcane', label: 'cropSugarcane' },
                            { id: 'Banana', label: 'cropBanana' },
                            { id: 'Coconut', label: 'cropCoconut' },
                            { id: 'Cotton', label: 'cropCotton' },
                            { id: 'Groundnut', label: 'cropGroundnut' },
                            { id: 'Millets', label: 'cropMillets' },
                            { id: 'Vegetables', label: 'cropVegetables' },
                            { id: 'Flowers', label: 'cropFlowers' },
                            { id: 'Other', label: 'others' }
                        ].map(crop => (
                            <label key={crop.id} className="flex items-center space-x-2 p-2 hover:bg-farm-green-50 rounded cursor-pointer transition-colors">
                                <input
                                    type="checkbox"
                                    checked={formData.crops.includes(crop.id)}
                                    onChange={() => handleCheckboxArray('crops', crop.id)}
                                    className="w-5 h-5 text-farm-green-600 border-gray-300 rounded focus:ring-farm-green-500"
                                />
                                <span className="text-sm md:text-base font-medium text-gray-700">{t(crop.label)}</span>
                            </label>
                        ))}
                    </div>
                    {formData.crops.includes('Other') && (
                        <div className="mt-4 animate-fade-in">
                            <label className="block text-lg font-semibold text-gray-700 mb-2">{t('specifyOther')}</label>
                            <input type="text" name="other_crops" value={formData.other_crops} onChange={handleChange}
                                className="input-field" placeholder="Enter other crops" />
                        </div>
                    )}
                </div>

                <div>
                    <label className="block text-lg font-semibold text-gray-700 mb-2">{t('soilType')}</label>
                    <select name="soil_type" value={formData.soil_type} onChange={handleChange} className="input-field" required>
                        <option value="">{t('selectOption')}</option>
                        <option value="Red">{t('soilRed')}</option>
                        <option value="Black">{t('soilBlack')}</option>
                        <option value="Alluvial">{t('soilAlluvial')}</option>
                        <option value="Clay">{t('soilClay')}</option>
                        <option value="Sandy">{t('soilSandy')}</option>
                        <option value="Loamy">{t('soilLoamy')}</option>
                        <option value="Laterite">{t('soilLaterite')}</option>
                        <option value="Saline">{t('soilSaline')}</option>
                        <option value="Alkaline">{t('soilAlkaline')}</option>
                        <option value="Gravelly">{t('soilGravelly')}</option>
                        <option value="Marshy">{t('soilMarshy')}</option>
                        <option value="Peaty">{t('soilPeaty')}</option>
                        <option value="Mixed">{t('soilMixed')}</option>
                        <option value="Other">Other / பிற</option>
                    </select>
                </div>

                {formData.soil_type === 'Other' && (
                    <div className="animate-fade-in">
                        <label className="block text-lg font-semibold text-gray-700 mb-2">{t('specifyOther')}</label>
                        <input type="text" name="other_soil_type" value={formData.other_soil_type} onChange={handleChange}
                            className="input-field" />
                    </div>
                )}

                <div>
                    <label className="block text-lg font-semibold text-gray-700 mb-2">{t('yieldHistory')}</label>
                    <select name="yield_history" value={formData.yield_history} onChange={handleChange} className="input-field" required>
                        <option value="">{t('selectOption')}</option>
                        <option value="Increasing">{t('yieldIncreasing')}</option>
                        <option value="Stable">{t('yieldStable')}</option>
                        <option value="Slight Decrease">{t('yieldSlightDecrease')}</option>
                        <option value="Decreasing">{t('yieldDecreasing')}</option>
                        <option value="Very Low">{t('yieldVeryLow')}</option>
                        <option value="Rainfall">{t('yieldRainfall')}</option>
                        <option value="Pests">{t('yieldPests')}</option>
                        <option value="Water Shortage">{t('yieldWaterShortage')}</option>
                        <option value="Soil Problems">{t('yieldSoilProblems')}</option>
                        <option value="First Year">{t('yieldFirstYear')}</option>
                        <option value="Varies">{t('yieldVaries')}</option>
                        <option value="Not Sure">{t('yieldNotSure')}</option>
                        <option value="Other">Other / பிற</option>
                    </select>
                </div>

                {formData.yield_history === 'Other' && (
                    <div className="animate-fade-in">
                        <label className="block text-lg font-semibold text-gray-700 mb-2">{t('specifyOther')}</label>
                        <input type="text" name="other_yield_history" value={formData.other_yield_history} onChange={handleChange}
                            className="input-field" />
                    </div>
                )}

                <div>
                    <label className="block text-lg font-semibold text-gray-700 mb-2">{t('marketLinkage')}</label>
                    <select name="market_linkage" value={formData.market_linkage} onChange={handleChange} className="input-field" required>
                        <option value="">{t('selectOption')}</option>
                        <option value="Local">{t('marketLocal')}</option>
                        <option value="Wholesale">{t('marketWholesale')}</option>
                        <option value="Direct">{t('marketDirect')}</option>
                        <option value="Online">{t('marketOnline')}</option>
                    </select>
                </div>
            </div>
        </div>
    );

    const renderStep3 = () => {
        const technologyOptions = [
            { id: 'Drip', label: 'techDrip' },
            { id: 'Sprinkler', label: 'techSprinkler' },
            { id: 'Mulching', label: 'techMulching' },
            { id: 'Greenhouse', label: 'techGreenhouse' },
            { id: 'ShadeNet', label: 'techShadenet' },
            { id: 'Tractor', label: 'techTractor' },
            { id: 'Harvester', label: 'techHarvester' },
            { id: 'Drone', label: 'techDrone' },
            { id: 'SoilKit', label: 'techSoilKit' },
            { id: 'MoistureSensor', label: 'techMoistureSensor' },
            { id: 'WeatherApp', label: 'techWeatherApp' },
            { id: 'UzhavanApp', label: 'uzhavanApp' },
            { id: 'DigitalPayment', label: 'techDigitalPayment' },
            { id: 'eNAM', label: 'usingEnam' },
            { id: 'Advisory', label: 'deptTraining' },
            { id: 'Insurance', label: 'techCropInsurance' },
            { id: 'SolarPump', label: 'techSolarPump' },
            { id: 'FarmMech', label: 'techMechanizationTools' },
            { id: 'None', label: 'techNone' },
            { id: 'Others', label: 'others' }
        ];

        return (
            <div className="space-y-6 animate-fade-in">
                <div className="text-center mb-6">
                    <div className="icon-container bg-farm-sky-100 text-farm-sky-600 mx-auto mb-3">
                        <FaMicrochip />
                    </div>
                    <h2 className="text-2xl font-bold text-farm-green-800">{t('step3')}</h2>
                </div>

                <div className="space-y-4">
                    <p className="text-lg font-semibold text-gray-700">{t('technologyUsage')}:</p>
                    <div className="grid md:grid-cols-2 gap-4">
                        {technologyOptions.map(tech => (
                            <label key={tech.id} className="flex items-center space-x-3 p-4 bg-white border-2 border-gray-200 rounded-lg hover:border-farm-green-400 cursor-pointer transition-all">
                                <input
                                    type="checkbox"
                                    checked={formData.technologies_used.includes(tech.id)}
                                    onChange={() => handleCheckboxArray('technologies_used', tech.id)}
                                    className="w-5 h-5 text-farm-green-600 border-gray-300 rounded focus:ring-farm-green-500"
                                />
                                <span className="text-lg font-medium text-gray-700">{t(tech.label)}</span>
                            </label>
                        ))}
                    </div>

                    {formData.technologies_used.includes('Others') && (
                        <div className="mt-6 animate-fade-in">
                            <label className="block text-lg font-semibold text-gray-700 mb-2">{t('specifyOther')}</label>
                            <input
                                type="text"
                                name="other_technology"
                                value={formData.other_technology}
                                onChange={handleChange}
                                className="input-field"
                                placeholder="Specify other technology"
                            />
                        </div>
                    )}
                </div>
            </div>
        );
    };

    const renderStep4 = () => {
        const schemes = [
            { id: 'PM-KISAN', label: { en: 'PM-KISAN', ta: 'பிஎம் கிசான் திட்டம்' } },
            { id: 'PMFBY', label: { en: 'PMFBY', ta: 'பிரதான் மந்திரி பயிர் காப்பீடு திட்டம்' } },
            { id: 'MSP', label: { en: 'MSP', ta: 'குறைந்தபட்ச ஆதரவு விலை' } },
            { id: 'Irrigation Subsidy', label: { en: 'Irrigation Subsidy', ta: 'பாசன உதவி தொகை' } },
            { id: 'Soil Health Card', label: { en: 'Soil Health Card', ta: 'மண் ஆரோக்கிய அட்டை' } },
            { id: 'KCC', label: { en: 'KCC', ta: 'கிசான் கிரெடிட் கார்டு' } },
            { id: 'eNAM', label: { en: 'eNAM', ta: 'தேசிய வேளாண் சந்தை' } },
            { id: 'Fasal Bima', label: { en: 'Fasal Bima', ta: 'பயிர் காப்பீடு திட்டம்' } }
        ];

        const tnSchemes = [
            { id: 'amma_two_wheeler_aware', label: 'ammaTwoWheeler' },
            { id: 'tn_micro_irrigation_aware', label: 'microIrrigation' },
            { id: 'tn_free_electricity_aware', label: 'freeElectricity' },
            { id: 'kalaignar_scheme_aware', label: 'kalaignarScheme' },
            { id: 'tn_soil_health_aware', label: 'soilHealth' },
            { id: 'tn_farm_mechanization_aware', label: 'farmMech' }
        ];

        return (
            <div className="space-y-6 animate-fade-in">
                <div className="text-center mb-6">
                    <div className="icon-container bg-farm-green-100 text-farm-green-600 mx-auto mb-3">
                        <FaUniversity />
                    </div>
                    <h2 className="text-2xl font-bold text-farm-green-800">{t('governmentSchemeAwareness')}</h2>
                </div>

                <div className="space-y-6">
                    <div>
                        <p className="text-lg font-semibold text-gray-700 mb-4">{t('centralGovtSchemeAwareness')}:</p>
                        <div className="grid md:grid-cols-2 gap-4">
                            {schemes.map(scheme => (
                                <label key={scheme.id} className="flex items-center space-x-3 p-4 bg-white border-2 border-gray-200 rounded-lg hover:border-farm-green-400 cursor-pointer transition-all">
                                    <input
                                        type="checkbox"
                                        checked={formData.schemes_aware.includes(scheme.id)}
                                        onChange={() => handleCheckboxArray('schemes_aware', scheme.id)}
                                    />
                                    <span className="text-lg">{scheme.label[language]}</span>
                                </label>
                            ))}

                            <label className="flex items-center space-x-3 p-4 bg-white border-2 border-gray-200 rounded-lg hover:border-farm-green-400 cursor-pointer transition-all">
                                <input
                                    type="checkbox"
                                    checked={formData.schemes_aware.includes('Others')}
                                    onChange={() => handleCheckboxArray('schemes_aware', 'Others')}
                                />
                                <span className="text-lg">Others / பிற</span>
                            </label>
                        </div>
                    </div>

                    {formData.schemes_aware.includes('Others') && (
                        <div className="mt-4 animate-fade-in">
                            <label className="block text-lg font-semibold text-gray-700 mb-2">{t('otherScheme')}</label>
                            <input
                                type="text"
                                name="other_scheme"
                                value={formData.other_scheme}
                                onChange={handleChange}
                                className="input-field"
                                placeholder="Specify other scheme"
                            />
                        </div>
                    )}

                    <div className="pt-6 border-t-2 border-gray-100">
                        <p className="text-lg font-semibold text-gray-700 mb-4">{t('tnGovtSchemeAwareness')}:</p>
                        <div className="grid md:grid-cols-2 gap-4">
                            {tnSchemes.map(scheme => (
                                <label key={scheme.id} className="flex items-center space-x-3 p-4 bg-farm-green-50 border-2 border-farm-green-200 rounded-lg hover:border-farm-green-400 cursor-pointer transition-all">
                                    <input
                                        type="checkbox"
                                        name={scheme.id}
                                        checked={formData[scheme.id]}
                                        onChange={handleChange}
                                        className="w-5 h-5 text-farm-green-600 rounded"
                                    />
                                    <span className="text-lg text-farm-green-900 font-medium">{t(scheme.label)}</span>
                                </label>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        );
    };

    const renderStep5 = () => (
        <div className="space-y-6 animate-fade-in">
            <div className="text-center mb-6">
                <div className="icon-container bg-farm-brown-100 text-farm-brown-600 mx-auto mb-3">
                    <FaMoneyBill />
                </div>
                <h2 className="text-2xl font-bold text-farm-green-800">{t('step5')}</h2>
            </div>

            <div className="space-y-6">
                {/* Savings & Risk Dropdowns */}
                <div className="grid md:grid-cols-2 gap-6">
                    <div>
                        <label className="block text-lg font-semibold text-gray-700 mb-2">{t('savingsHabit')}</label>
                        <select name="savings_habit" value={formData.savings_habit} onChange={handleChange} className="input-field" required>
                            <option value="">{t('selectOption')}</option>
                            <option value="Regularly">{t('saveRegularly')}</option>
                            <option value="Occasionally">{t('saveOccasionally')}</option>
                            <option value="Rarely">{t('saveRarely')}</option>
                            <option value="No Savings">{t('saveNoSavings')}</option>
                            <option value="Other">{t('others')}</option>
                        </select>
                    </div>

                    <div>
                        <label className="block text-lg font-semibold text-gray-700 mb-2">{t('riskLevel')}</label>
                        <select name="risk_level" value={formData.risk_level} onChange={handleChange} className="input-field" required>
                            <option value="">{t('selectOption')}</option>
                            <option value="Very High">{t('riskVeryHigh')}</option>
                            <option value="High">{t('riskHigh')}</option>
                            <option value="Medium">{t('riskMedium')}</option>
                            <option value="Low">{t('riskLow')}</option>
                            <option value="Very Low">{t('riskVeryLow')}</option>
                            <option value="Other">{t('others')}</option>
                        </select>
                    </div>
                </div>

                {/* Credit & Loan */}
                <div className="p-4 bg-white border-2 border-gray-100 rounded-lg space-y-4">
                    <h3 className="text-xl font-bold text-farm-green-700 border-b pb-2">💰 {t('loanTaken')}</h3>
                    <div className="flex items-center space-x-4">
                        <label className="flex items-center space-x-2">
                            <input type="radio" name="has_loan" value="true" checked={formData.has_loan === true || formData.has_loan === "true"} onChange={() => setFormData({ ...formData, has_loan: true })} />
                            <span>{t('yes')}</span>
                        </label>
                        <label className="flex items-center space-x-2">
                            <input type="radio" name="has_loan" value="false" checked={formData.has_loan === false || formData.has_loan === "false"} onChange={() => setFormData({ ...formData, has_loan: false })} />
                            <span>{t('no')}</span>
                        </label>
                    </div>
                    {formData.has_loan && (
                        <div className="grid md:grid-cols-2 gap-4 animate-fade-in">
                            <div>
                                <label className="block font-semibold mb-1">{t('loanSource')}</label>
                                <select name="loan_source" value={formData.loan_source} onChange={handleChange} className="input-field">
                                    <option value="">{t('selectOption')}</option>
                                    <option value="Bank">{t('loanBank')}</option>
                                    <option value="Cooperative">{t('loanCooperative')}</option>
                                    <option value="Private">{t('loanPrivate')}</option>
                                    <option value="None">{t('loanNone')}</option>
                                </select>
                            </div>
                            <div className="flex items-center space-x-4 h-full pt-6">
                                <input type="checkbox" name="repay_on_time" checked={formData.repay_on_time} onChange={handleChange} id="repay" />
                                <label htmlFor="repay" className="font-semibold">{t('repayOnTime')}</label>
                            </div>
                        </div>
                    )}
                </div>

                {/* Insurance */}
                <div className="p-4 bg-white border-2 border-gray-100 rounded-lg space-y-4">
                    <h3 className="text-xl font-bold text-farm-green-700 border-b pb-2">🛡️ {t('hasInsurance')}</h3>
                    <div className="grid md:grid-cols-2 gap-4">
                        <label className="flex items-center space-x-3">
                            <input type="checkbox" name="enrolled_pmfby" checked={formData.enrolled_pmfby} onChange={handleChange} />
                            <span>{t('enrolledPMFBY')}</span>
                        </label>
                        <label className="flex items-center space-x-3">
                            <input type="checkbox" name="crop_loss_earlier" checked={formData.crop_loss_earlier} onChange={handleChange} />
                            <span>{t('cropLossEarlier')}</span>
                        </label>
                    </div>
                </div>

                {/* Income & Stability */}
                <div className="p-4 bg-white border-2 border-gray-100 rounded-lg space-y-4">
                    <h3 className="text-xl font-bold text-farm-green-700 border-b pb-2">💵 {t('income')} & Stability</h3>
                    <div className="grid md:grid-cols-2 gap-4">
                        <label className="flex items-center space-x-3">
                            <input type="checkbox" name="farming_only_income" checked={formData.farming_only_income} onChange={handleChange} />
                            <span>{t('farmingOnlyIncome')}</span>
                        </label>
                        <label className="flex items-center space-x-3">
                            <input type="checkbox" name="has_other_income" checked={formData.has_other_income} onChange={handleChange} />
                            <span>{t('hasOtherIncome')}</span>
                        </label>
                    </div>
                </div>

                {/* Savings & Investment */}
                <div className="p-4 bg-white border-2 border-gray-100 rounded-lg space-y-4">
                    <h3 className="text-xl font-bold text-farm-green-700 border-b pb-2">🏦 {t('savingsHabit')} & Investment</h3>
                    <label className="flex items-center space-x-3">
                        <input type="checkbox" name="save_after_harvest" checked={formData.save_after_harvest} onChange={handleChange} />
                        <span>{t('saveAfterHarvest')}</span>
                    </label>
                    {formData.save_after_harvest && (
                        <div className="animate-fade-in">
                            <label className="block font-semibold mb-1">{t('whereSave')}</label>
                            <select name="saving_location" value={formData.saving_location} onChange={handleChange} className="input-field">
                                <option value="">{t('selectOption')}</option>
                                <option value="Bank">{t('saveBank')}</option>
                                <option value="Home">{t('saveHome')}</option>
                                <option value="Chit Fund">{t('saveChit')}</option>
                                <option value="SHG">{t('saveSHG')}</option>
                                <option value="None">{t('saveNone')}</option>
                            </select>
                        </div>
                    )}
                    <label className="flex items-center space-x-3">
                        <input type="checkbox" name="invested_equipment" checked={formData.invested_equipment} onChange={handleChange} />
                        <span>{t('investedEquipment')}</span>
                    </label>
                </div>

                {/* Digital & Payment Behaviour */}
                <div className="p-4 bg-white border-2 border-gray-100 rounded-lg space-y-4">
                    <h3 className="text-xl font-bold text-farm-green-700 border-b pb-2">📱 Digital & Payment</h3>
                    <div className="grid md:grid-cols-2 gap-4">
                        <label className="flex items-center space-x-3">
                            <input type="checkbox" name="digital_payment_usage" checked={formData.digital_payment_usage} onChange={handleChange} />
                            <span>{t('digitalPaymentUsage')}</span>
                        </label>
                        <label className="flex items-center space-x-3">
                            <input type="checkbox" name="check_market_price" checked={formData.check_market_price} onChange={handleChange} />
                            <span>{t('checkMarketPrice')}</span>
                        </label>
                    </div>
                </div>
            </div>
        </div>
    );

    const renderStep6 = () => (
        <div className="space-y-6 animate-fade-in">
            <div className="text-center mb-6">
                <div className="icon-container bg-farm-sky-100 text-farm-sky-600 mx-auto mb-3">
                    <FaHeart />
                </div>
                <h2 className="text-2xl font-bold text-farm-green-800">{t('step5')}</h2>
                <div className="flex justify-between text-xs text-gray-500 max-w-md mx-auto mt-2">
                    <span>{t('scaleStronglyDisagree')}</span>
                    <span>{t('scaleStronglyAgree')}</span>
                </div>
            </div>

            <div className="space-y-8">
                <div>
                    <label className="block text-lg font-semibold text-gray-700 mb-3">
                        {t('riskTryNewMethods')}
                    </label>
                    <div className="flex items-center space-x-4">
                        <span>1</span>
                        <input
                            type="range"
                            min="1"
                            max="5"
                            value={formData.risk_try_new_methods}
                            onChange={(e) => handleSlider('risk_try_new_methods', e.target.value)}
                            className="flex-1"
                        />
                        <span>5</span>
                        <span className="text-2xl font-bold text-farm-green-600 ml-4">{formData.risk_try_new_methods}</span>
                    </div>
                </div>

                <div>
                    <label className="block text-lg font-semibold text-gray-700 mb-3">
                        {t('riskAfraidLoss')}
                    </label>
                    <div className="flex items-center space-x-4">
                        <span>1</span>
                        <input
                            type="range"
                            min="1"
                            max="5"
                            value={formData.risk_afraid_loss}
                            onChange={(e) => handleSlider('risk_afraid_loss', e.target.value)}
                            className="flex-1"
                        />
                        <span>5</span>
                        <span className="text-2xl font-bold text-farm-green-600 ml-4">{formData.risk_afraid_loss}</span>
                    </div>
                </div>

                <div>
                    <label className="block text-lg font-semibold text-gray-700 mb-3">
                        {t('riskFollowNeighbors')}
                    </label>
                    <div className="flex items-center space-x-4">
                        <span>1</span>
                        <input
                            type="range"
                            min="1"
                            max="5"
                            value={formData.risk_follow_neighbors}
                            onChange={(e) => handleSlider('risk_follow_neighbors', e.target.value)}
                            className="flex-1"
                        />
                        <span>5</span>
                        <span className="text-2xl font-bold text-farm-green-600 ml-4">{formData.risk_follow_neighbors}</span>
                    </div>
                </div>

                <div className="pt-6 border-t border-gray-100">
                    <p className="text-center font-bold text-gray-400 mb-4 uppercase tracking-widest text-sm">Legacy Metrics</p>
                    <div className="space-y-6 opacity-60">
                        <div>
                            <label className="block text-base font-medium text-gray-600 mb-2">Openness to New Tech</label>
                            <input type="range" min="1" max="5" value={formData.openness} onChange={(e) => handleSlider('openness', e.target.value)} className="w-full" />
                        </div>
                        <div>
                            <label className="block text-base font-medium text-gray-600 mb-2">Trust in Technology</label>
                            <input type="range" min="1" max="5" value={formData.trust} onChange={(e) => handleSlider('trust', e.target.value)} className="w-full" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );

    const renderStep7 = () => (
        <div className="space-y-6 animate-fade-in">
            <div className="text-center mb-6">
                <div className="icon-container bg-farm-green-100 text-farm-green-600 mx-auto mb-3">
                    <FaLandmark />
                </div>
                <h2 className="text-2xl font-bold text-farm-green-800">{t('step7')}</h2>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
                <div>
                    <label className="block text-lg font-semibold text-gray-700 mb-2">{t('block')}</label>
                    <input type="text" name="block" value={formData.block} onChange={handleChange} className="input-field" />
                </div>
                <div>
                    <label className="block text-lg font-semibold text-gray-700 mb-2">{t('village')}</label>
                    <input type="text" name="village" value={formData.village} onChange={handleChange} className="input-field" />
                </div>
                <div>
                    <label className="block text-lg font-semibold text-gray-700 mb-2">{t('agroZone')}</label>
                    <select name="agro_climatic_zone" value={formData.agro_climatic_zone} onChange={handleChange} className="input-field">
                        <option value="">{t('selectOption')}</option>
                        <option value="Delta">{t('zoneDelta')}</option>
                        <option value="Dry">{t('zoneDry')}</option>
                        <option value="Hilly">{t('zoneHilly')}</option>
                        <option value="Coastal">{t('zoneCoastal')}</option>
                        <option value="Other">Other / பிற</option>
                    </select>
                </div>
                {formData.agro_climatic_zone === 'Other' && (
                    <div className="animate-fade-in">
                        <label className="block text-lg font-semibold text-gray-700 mb-2">{t('specifyOther')}</label>
                        <input type="text" name="other_agro_climatic_zone" value={formData.other_agro_climatic_zone} onChange={handleChange}
                            className="input-field" />
                    </div>
                )}
                <div>
                    <label className="block text-lg font-semibold text-gray-700 mb-2">{t('farmerCategory')}</label>
                    <select name="farmer_category" value={formData.farmer_category} onChange={handleChange} className="input-field">
                        <option value="">{t('selectOption')}</option>
                        <option value="Small / Marginal">{t('smallMarginal')}</option>
                        <option value="Medium / Large">{t('mediumLarge')}</option>
                        <option value="Other">Other / பிற</option>
                    </select>
                </div>
                {formData.farmer_category === 'Other' && (
                    <div className="animate-fade-in">
                        <label className="block text-lg font-semibold text-gray-700 mb-2">{t('specifyOther')}</label>
                        <input type="text" name="other_farmer_category" value={formData.other_farmer_category} onChange={handleChange}
                            className="input-field" />
                    </div>
                )}
                <div className="flex items-center space-x-4 p-4 bg-white border-2 border-gray-200 rounded-lg">
                    <input type="checkbox" name="farmer_smart_card" checked={formData.farmer_smart_card} onChange={handleChange} />
                    <label className="text-lg font-semibold">{t('smartCard')}</label>
                </div>
            </div>
        </div>
    );

    const renderStep8 = () => (
        <div className="space-y-6 animate-fade-in">
            <div className="text-center mb-6">
                <div className="icon-container bg-farm-sky-100 text-farm-sky-600 mx-auto mb-3">
                    <FaMicrochip />
                </div>
                <h2 className="text-2xl font-bold text-farm-green-800">{t('step6')}</h2>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
                <div>
                    <label className="block text-lg font-semibold text-gray-700 mb-2">{t('borewellDepth')}</label>
                    <input type="number" name="borewell_depth" value={formData.borewell_depth} onChange={handleChange}
                        className="input-field" placeholder={t('borewellDepthPlaceholder')} />
                </div>

                <div>
                    <label className="block text-lg font-semibold text-gray-700 mb-2">{t('scarcityMonths')}</label>
                    <select name="water_scarcity_months" value={formData.water_scarcity_months} onChange={handleChange} className="input-field">
                        <option value="0">{t('scarcity0')}</option>
                        <option value="1-3">{t('scarcity1_3')}</option>
                        <option value="4-6">{t('scarcity4_6')}</option>
                        <option value="7-9">{t('scarcity7_9')}</option>
                        <option value="10-12">{t('scarcity10_12')}</option>
                    </select>
                </div>

                <div>
                    <label className="block text-lg font-semibold text-gray-700 mb-2">{t('primaryIrrigationSource')}</label>
                    <select name="irrigation_source" value={formData.irrigation_source} onChange={handleChange} className="input-field">
                        <option value="">{t('selectOption')}</option>
                        <option value="Borewell">{t('irriBorewell')}</option>
                        <option value="Canal">{t('irriCanal')}</option>
                        <option value="River">{t('irriRiver')}</option>
                        <option value="Rainfed">{t('irriRainfed')}</option>
                        <option value="Farm Pond">{t('irriFarmPond')}</option>
                        <option value="Other">{t('others')}</option>
                    </select>
                </div>

                {formData.irrigation_source === 'Other' && (
                    <div className="animate-fade-in md:col-span-2">
                        <label className="block text-lg font-semibold text-gray-700 mb-2">{t('specifyOther')}</label>
                        <input type="text" name="other_irrigation_source" value={formData.other_irrigation_source} onChange={handleChange}
                            className="input-field" placeholder={t('specifyOther')} />
                    </div>
                )}

                <div>
                    <label className="block text-lg font-semibold text-gray-700 mb-2">{t('irrigationMethodUsed')}</label>
                    <select name="water_availability" value={formData.water_availability} onChange={handleChange} className="input-field">
                        <option value="">{t('selectOption')}</option>
                        <option value="Flood">{t('methodFlood')}</option>
                        <option value="Drip">{t('methodDrip')}</option>
                        <option value="Sprinkler">{t('methodSprinkler')}</option>
                        <option value="Manual">{t('methodManual')}</option>
                        <option value="Mixed">{t('methodMixed')}</option>
                    </select>
                </div>
            </div>
        </div>
    );

    const renderStep9 = () => (
        <div className="space-y-6 animate-fade-in">
            <div className="text-center mb-6">
                <div className="icon-container bg-farm-brown-100 text-farm-brown-600 mx-auto mb-3">
                    <FaUniversity />
                </div>
                <h2 className="text-2xl font-bold text-farm-green-800">{t('step7')}</h2>
            </div>

            <div className="space-y-6">
                <div className="grid md:grid-cols-2 gap-4">
                    <div className="flex items-center space-x-4 p-4 bg-white border-2 border-gray-200 rounded-lg">
                        <input type="checkbox" name="selling_uzhavar_sandhai" checked={formData.selling_uzhavar_sandhai} onChange={handleChange} />
                        <label className="font-semibold">{t('uzhavarSandhai')}</label>
                    </div>
                    <div className="flex items-center space-x-4 p-4 bg-white border-2 border-gray-200 rounded-lg">
                        <input type="checkbox" name="using_enam" checked={formData.using_enam} onChange={handleChange} />
                        <label className="font-semibold">{t('usingEnam')}</label>
                    </div>
                </div>

                <div>
                    <label className="block text-lg font-semibold text-gray-700 mb-2">{t('marketLinkage')}</label>
                    <select name="market_type" value={formData.market_type} onChange={handleChange} className="input-field">
                        <option value="">{t('selectOption')}</option>
                        <option value="Direct">{t('marketDirect')}</option>
                        <option value="Middleman">{t('marketMiddleman')}</option>
                        <option value="Other">Other / பிற</option>
                    </select>
                </div>
                {formData.market_type === 'Other' && (
                    <div className="animate-fade-in">
                        <label className="block text-lg font-semibold text-gray-700 mb-2">{t('specifyOther')}</label>
                        <input type="text" name="other_market_type" value={formData.other_market_type} onChange={handleChange}
                            className="input-field" />
                    </div>
                )}
            </div>

            <div className="pt-4 border-t-2 border-gray-100">
                <p className="font-bold text-gray-800 mb-3">{t('trainingDigitalUsage')}:</p>
                <div className="grid md:grid-cols-3 gap-3">
                    {[
                        { id: 'attended_training', label: 'deptTraining' },
                        { id: 'met_vao_aeo', label: 'metVAO' },
                        { id: 'visited_tnau_farm', label: 'visitedTNAU' },
                        { id: 'read_tamil', label: 'readTamil' },
                        { id: 'read_english', label: 'readEnglish' },
                        { id: 'voice_guidance_pref', label: 'voiceGuidance' },
                        { id: 'using_uzhavan_app', label: 'uzhavanApp' },
                        { id: 'watch_agri_youtube', label: 'agriYoutube' },
                        { id: 'in_whatsapp_groups', label: 'whatsappGroups' }
                    ].map(item => (
                        <label key={item.id} className="flex items-center space-x-2 p-3 bg-gray-50 rounded border border-gray-200">
                            <input type="checkbox" name={item.id} checked={formData[item.id]} onChange={handleChange} />
                            <span className="text-sm">{t(item.label)}</span>
                        </label>
                    ))}
                </div>
            </div>
        </div>
    );

    return (
        <div className="min-h-screen p-4 py-12 flex flex-col items-center">
            {/* Project Branding */}
            <div className="text-center mb-8 animate-fade-in">
                <h1 className="text-4xl font-bold text-farm-green-700 flex items-center justify-center gap-2 mb-2">
                    {t('appName')}
                </h1>
                <p className="text-sm text-gray-500 font-semibold tracking-wider uppercase">
                    {t('appSubtitle')}
                </p>
            </div>

            <div className="max-w-4xl w-full mx-auto">
                <div className="card shadow-2xl animate-fade-in mb-8">
                    {renderProgressBar()}

                    {error && (
                        <div className="bg-red-100 border-2 border-red-400 text-red-700 px-4 py-3 rounded-lg mb-6">
                            {error}
                        </div>
                    )}

                    {currentStep === 1 && renderStep1()}
                    {currentStep === 2 && renderStep2()}
                    {currentStep === 3 && renderStep3()}
                    {currentStep === 4 && renderStep4()}
                    {currentStep === 5 && renderStep6()}
                    {currentStep === 6 && renderStep8()}
                    {currentStep === 7 && renderStep9()}

                    {/* Navigation Buttons */}
                    <div className="flex justify-between mt-8 pt-6 border-t-2 border-gray-200">
                        {currentStep > 1 && (
                            <button onClick={prevStep} className="btn-outline">
                                <FaArrowLeft /> {t('previous')}
                            </button>
                        )}

                        {currentStep < totalSteps ? (
                            <button onClick={nextStep} className="btn-primary ml-auto">
                                {t('next')} <FaArrowRight />
                            </button>
                        ) : (
                            <button onClick={handleSubmit} disabled={loading} className="btn-primary ml-auto">
                                {loading ? 'Submitting...' : <><FaCheck /> {t('submit')}</>}
                            </button>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default FarmerForm;
