import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { complaintsAPI } from '../../api/complaints';
import { productsAPI } from '../../api/products';
import { addComplaint, updateComplaint } from '../../store/slices/complaintSlice';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';
import Select from '../../components/common/Select';
import Card from '../../components/common/Card';
import CardContent from '../../components/common/CardContent';
import CardFooter from '../../components/common/CardFooter';
import Spinner from '../../components/common/Spinner';
import toast from 'react-hot-toast';

const ComplaintForm = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const isEdit = !!id;
  const [loading, setLoading] = useState(false);
  const [products, setProducts] = useState([]);
  const [formData, setFormData] = useState({
    product_id: '',
    description: '',
    reporter_name: '',
    reporter_email: '',
    reporter_phone: '',
    batch_lot_no: '',
    received_date: new Date().toISOString().split('T')[0],
    priority: 'medium',
    category: '',
  });

  useEffect(() => {
    fetchProducts();
    if (isEdit) {
      fetchComplaint();
    }
  }, [id, isEdit]);

  const fetchProducts = async () => {
    try {
      const data = await productsAPI.list();
      setProducts(data);
    } catch (error) {
      console.error('Failed to fetch products:', error);
    }
  };

  const fetchComplaint = async () => {
    try {
      const data = await complaintsAPI.get(id);
      setFormData({
        product_id: data.product_id || '',
        description: data.description || '',
        reporter_name: data.reporter_name || '',
        reporter_email: data.reporter_email || '',
        reporter_phone: data.reporter_phone || '',
        batch_lot_no: data.batch_lot_no || '',
        received_date: data.received_date || '',
        priority: data.priority || 'medium',
        category: data.category || '',
      });
    } catch (error) {
      console.error('Failed to fetch complaint:', error);
      toast.error('Failed to load complaint');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      if (isEdit) {
        const data = await complaintsAPI.update(id, formData);
        dispatch(updateComplaint(data));
        toast.success('Complaint updated successfully');
      } else {
        const data = await complaintsAPI.create(formData);
        dispatch(addComplaint(data));
        toast.success('Complaint created successfully');
      }
      navigate('/complaints');
    } catch (error) {
      console.error('Failed to save complaint:', error);
      toast.error('Failed to save complaint');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const categoryOptions = [
    { value: '', label: 'Select Category' },
    { value: 'quality', label: 'Quality' },
    { value: 'safety', label: 'Safety' },
    { value: 'packaging', label: 'Packaging' },
    { value: 'labeling', label: 'Labeling' },
    { value: 'efficacy', label: 'Efficacy' },
  ];

  const priorityOptions = [
    { value: 'low', label: 'Low' },
    { value: 'medium', label: 'Medium' },
    { value: 'high', label: 'High' },
    { value: 'critical', label: 'Critical' },
  ];

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
        {isEdit ? 'Edit Complaint' : 'New Complaint'}
      </h1>

      <Card>
        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-6">
            <Select
              label="Product"
              options={[{ value: '', label: 'Select Product' }, ...products.map(p => ({ value: p.id, label: p.product_name }))]}
              value={formData.product_id}
              onChange={(e) => handleChange({ target: { name: 'product_id', value: e.target.value } })}
            />

            <Select
              label="Priority"
              options={priorityOptions}
              value={formData.priority}
              onChange={(e) => handleChange({ target: { name: 'priority', value: e.target.value } })}
            />

            <Select
              label="Category"
              options={categoryOptions}
              value={formData.category}
              onChange={(e) => handleChange({ target: { name: 'category', value: e.target.value } })}
            />

            <Input
              label="Description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              required
              multiline
              rows={4}
              placeholder="Describe the complaint in detail"
            />

            <Input
              label="Reporter Name"
              name="reporter_name"
              value={formData.reporter_name}
              onChange={handleChange}
              placeholder="Name of the person reporting"
            />

            <Input
              label="Reporter Email"
              name="reporter_email"
              type="email"
              value={formData.reporter_email}
              onChange={handleChange}
              placeholder="Email of the reporter"
            />

            <Input
              label="Reporter Phone"
              name="reporter_phone"
              value={formData.reporter_phone}
              onChange={handleChange}
              placeholder="Phone number of the reporter"
            />

            <Input
              label="Batch/Lot Number"
              name="batch_lot_no"
              value={formData.batch_lot_no}
              onChange={handleChange}
              placeholder="Batch or lot number"
            />

            <Input
              label="Received Date"
              name="received_date"
              type="date"
              value={formData.received_date}
              onChange={handleChange}
              required
            />
          </CardContent>

          <CardFooter className="flex justify-end gap-3">
            <Button
              type="button"
              variant="secondary"
              onClick={() => navigate('/complaints')}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={loading}>
              {loading ? <Spinner size="sm" /> : (isEdit ? 'Update' : 'Create')}
            </Button>
          </CardFooter>
        </form>
      </Card>
    </div>
  );
};

export default ComplaintForm;
