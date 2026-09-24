from pathlib import Path
import argparse,json,os,resource,time,unittest
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
if hasattr(os,'sched_setaffinity'):os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
resource.setrlimit(resource.RLIMIT_AS,(3584*1024**2,3584*1024**2));resource.setrlimit(resource.RLIMIT_CPU,(40,40))
t=time.process_time();wall=time.perf_counter()
suite=unittest.defaultTestLoader.discover(str(Path(__file__).resolve().parent),pattern='test_*.py')
r=unittest.TextTestRunner(verbosity=2).run(suite)
report={'test_methods':r.testsRun,'failures':len(r.failures),'errors':len(r.errors),'successful':r.wasSuccessful(),
        'measurement':{'cpu_seconds':time.process_time()-t,'wall_seconds':time.perf_counter()-wall,
                       'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'workers':1}}
args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
raise SystemExit(0 if r.wasSuccessful() else 1)
