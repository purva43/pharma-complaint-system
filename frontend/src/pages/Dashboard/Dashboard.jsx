import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { complaintsAPI } from '../../api/complaints';
import { setComplaints, setLoading } from '../../store/slices/complaintSlice';
import Card from '../../components/common/Card';
import CardContent from '../../components/common/Card';
import { FileText, AlertTriangle, CheckCircle, Clock } from 'lucide-react';

const Dashboard = () => {
  const dispatch = useDispatch();
  const { complaints } = useSelector((state) => state.complaints);

  useEffect(() => {
    const fetchComplaints = async () => {
      dispatch(setLoading(true));
      try {
        const data = await complaintsAPI.list({ limit: 10 });
        dispatch(setComplaints(data));
      } catch (error) {
        console.error('Failed to fetch complaints:', error);
      } finally {
        dispatch(setLoading(false));
      }
    };

    fetchComplaints();
  }, [dispatch]);

  const stats = [
    {
      label: 'Total Complaints',
      value: complaints.length,
      icon: FileText,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
    },
    {
      label: 'Open',
      value: complaints.filter(c => c.status === 'under_investigation').length,
      icon: AlertTriangle,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-100',
    },
    {
      label: 'Closed',
      value: complaints.filter(c => c.status === 'closed').length,
      icon: CheckCircle,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
    },
    {
      label: 'Pending',
      value: complaints.filter(c => c.status === 'submitted').length,
      icon: Clock,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
    },
  ];

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
        Dashboard
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat) => (
          <Card key={stat.label}>
            <CardContent>
              <div className="flex items-center gap-4">
                <div className={`p-3 rounded-lg ${stat.bgColor}`}>
                  <stat.icon className={stat.color} size={24} />
                </div>
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">{stat.label}</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    {stat.value}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card>
        <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
            Recent Complaints
          </h2>
        </div>
        <div className="p-6">
          {complaints.length === 0 ? (
            <p className="text-gray-500 dark:text-gray-400 text-center py-8">
              No complaints yet
            </p>
          ) : (
            <div className="space-y-4">
              {complaints.slice(0, 5).map((complaint) => (
                <div
                  key={complaint.id}
                  className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg"
                >
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white">
                      {complaint.complaint_no}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {complaint.description?.substring(0, 50)}...
                    </p>
                  </div>
                  <span className="text-sm text-gray-500 dark:text-gray-400">
                    {complaint.status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </Card>
    </div>
  );
};

export default Dashboard;
