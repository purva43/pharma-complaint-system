import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { complaintsAPI } from '../../api/complaints';
import { setComplaints, setLoading, setFilters } from '../../store/slices/complaintSlice';
import Button from '../../components/common/Button';
import Card from '../../components/common/Card';
import Badge from '../../components/common/Badge';
import Spinner from '../../components/common/Spinner';
import Select from '../../components/common/Select';
import { Search, Plus } from 'lucide-react';

const ComplaintList = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { complaints, loading, filters } = useSelector((state) => state.complaints);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchComplaints();
  }, [filters]);

  const fetchComplaints = async () => {
    dispatch(setLoading(true));
    try {
      const data = await complaintsAPI.list(filters);
      dispatch(setComplaints(data));
    } catch (error) {
      console.error('Failed to fetch complaints:', error);
    } finally {
      dispatch(setLoading(false));
    }
  };

  const handleFilterChange = (key, value) => {
    dispatch(setFilters({ [key]: value }));
  };

  const filteredComplaints = complaints.filter(complaint =>
    complaint.complaint_no.toLowerCase().includes(searchTerm.toLowerCase()) ||
    complaint.description?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const statusOptions = [
    { value: '', label: 'All Statuses' },
    { value: 'draft', label: 'Draft' },
    { value: 'submitted', label: 'Submitted' },
    { value: 'under_investigation', label: 'Under Investigation' },
    { value: 'pending_capa', label: 'Pending CAPA' },
    { value: 'closed', label: 'Closed' },
  ];

  const priorityOptions = [
    { value: '', label: 'All Priorities' },
    { value: 'low', label: 'Low' },
    { value: 'medium', label: 'Medium' },
    { value: 'high', label: 'High' },
    { value: 'critical', label: 'Critical' },
  ];

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Complaints
        </h1>
        <Button onClick={() => navigate('/complaints/new')}>
          <Plus size={20} className="mr-2" />
          New Complaint
        </Button>
      </div>

      <Card className="mb-6">
        <CardContent>
          <div className="flex flex-wrap gap-4 items-end">
            <div className="flex-1 min-w-[200px]">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                <input
                  type="text"
                  placeholder="Search complaints..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-gray-800 dark:border-gray-600 dark:text-white"
                />
              </div>
            </div>
            <Select
              options={statusOptions}
              value={filters.status}
              onChange={(e) => handleFilterChange('status', e.target.value)}
              className="min-w-[150px]"
            />
            <Select
              options={priorityOptions}
              value={filters.priority}
              onChange={(e) => handleFilterChange('priority', e.target.value)}
              className="min-w-[150px]"
            />
          </div>
        </CardContent>
      </Card>

      <Card>
        {loading ? (
          <div className="flex justify-center py-12">
            <Spinner size="lg" />
          </div>
        ) : filteredComplaints.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 dark:text-gray-400">No complaints found</p>
          </div>
        ) : (
          <div className="divide-y divide-gray-200 dark:divide-gray-700">
            {filteredComplaints.map((complaint) => (
              <div
                key={complaint.id}
                className="p-6 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer transition-colors"
                onClick={() => navigate(`/complaints/${complaint.id}`)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="font-semibold text-gray-900 dark:text-white">
                        {complaint.complaint_no}
                      </h3>
                      <Badge variant={complaint.priority === 'critical' ? 'danger' : 'default'}>
                        {complaint.priority}
                      </Badge>
                      <Badge variant="primary">{complaint.status}</Badge>
                    </div>
                    <p className="text-gray-600 dark:text-gray-400 mb-2">
                      {complaint.description}
                    </p>
                    <div className="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400">
                      <span>Received: {complaint.received_date}</span>
                      {complaint.category && <span>Category: {complaint.category}</span>}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
};

export default ComplaintList;
