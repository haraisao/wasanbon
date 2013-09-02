import sys, os, time

import wasanbon
from wasanbon.core import tools 
#from wasanbon.core import system
#from xml.etree import ElementTree
from wasanbon.core import project as prj

from rtshell import rtcryo

def save_all_system(nameservers, filepath='system/DefaultSystem.xml', verbose=False):
    if verbose:
        sys.stdout.write(" - Saving System on %s to %s\n" % (str(nameservers), filepath))
    for i in range(0, 5):
        try:
            argv = ['--verbose', '-n', 'DefaultSystem01', '-v', '1.0', '-e', 'Sugar Sweet Robotics',  '-o', filepath]
            argv = argv + nameservers
            rtcryo.main(argv=argv)
            sys.stdout.write(' - Saved.\n')
            return
        except omniORB.CORBA.UNKNOWN, e:
            #traceback.print_exc()
            pass
        except Exception, e:
            pass


class Command(object):
    def __init__(self):
        pass


    def execute_with_argv(self, argv, verbose, clean, force):
        wasanbon.arg_check(argv, 3)

        proj = prj.Project(os.getcwd())

        if(argv[2] == 'eclipse'):
            print 'Launching Eclipse'
            tools.launch_eclipse(proj.rtc_path, verbose=verbose)
            return
        elif(argv[2] == 'arduino'):
            print '- Launching Arduino'
            tools.launch_arduino(".", verbose=verbose)
            return
        elif argv[2] == 'RTno':
            sys.stdout.write(' - RTno\n')
            wasanbon.arg_check(argv, 4)
            if argv[3] == 'template':
                # wasanbon.arg_check(argv, 5)
                rtc_name = argv[4]
                tools.generate_rtno_temprate(proj, rtc_name, verbose=verbose)

        elif(argv[2] == 'rtcb'):
            print 'Launching Eclipse'
            tools.launch_eclipse(proj.rtc_path, verbose=verbose)
            return

        elif(argv[2] == 'rtse'):
            sys.stdout.write(' @ Launching Eclipse\n')
            nss = proj.get_nameservers(verbose=verbose)
            for ns in nss:
                if not ns.check_and_launch(verbose=verbose, force=force):
                    sys.stdout.write(' @ NameService %s is not running\n' % ns.path)
                    return False

            for i in range(0, 5):
                sys.stdout.write('\r - Waiting (%s/%s)\n' % (i+1, 5))
                sys.stdout.flush()
                time.sleep(1)

            
            proj.launch_all_rtcd(verbose=verbose)
            #tools.launch_eclipse(proj.system_path, nonblock=False, verbose=verbose)
            tools.launch_eclipse(nonblock=False, verbose=verbose)

            for i in range(0, 5):
                sys.stdout.write('\r - Waiting (%s/%s)\n' % (i+1, 5))
                sys.stdout.flush()
                time.sleep(1)

            for ns in nss:
                ns.refresh(verbose=verbose, force=True)
                
            #pairs = proj.available_connection_pairs(nameservers=nss, verbose=verbose)
            
            ns_addrs = [ns.path for ns in nss]
            save_all_system(['localhost'])

            for i in range(0, 5):
                sys.stdout.write('\r - Waiting (%s/%s)\n' % (i+1, 5))
                sys.stdout.flush()
                time.sleep(1)

            proj.terminate_all_rtcd(verbose=verbose)
            
            for ns in nss:
                ns.kill()
        else:
            raise wasanbon.InvalidUsageException()
